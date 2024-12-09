# Imports padronizados
from uuid import UUID
from datetime import datetime, timedelta

# Imports do Django
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, now

# Imports de terceiros
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa
import pytz

# Imports locais
from .models import WorkPoint
from .serializers import WorkPointSerializer
from .utils import (
    calculate_extra_hours,
    calculate_remaining_hours,
    calculate_worked_hours,
)

User = get_user_model()


class UserPermissionMixin:
    """Mixin para verificar permissões e retornar o usuário autorizado."""

    def get_user(self, request, user_id=None):
        if user_id:
            user_id = self.validate_uuid(user_id)
            if request.user.is_staff or request.user.id == user_id:
                return get_object_or_404(User, id=user_id)
            raise PermissionDenied("Você não tem permissão para acessar este usuário.")
        return request.user

    @staticmethod
    def validate_uuid(user_id):
        if isinstance(user_id, UUID):
            return user_id
        try:
            return UUID(user_id)
        except ValueError:
            raise NotFound("ID inválido.")


class DateValidationMixin:
    """Mixin para validar parâmetros de data."""

    @staticmethod
    def validate_date_params(start_date, end_date):
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")

        if start_date > end_date:
            raise ValueError("'start_date' não pode ser maior que 'end_date'.")

        return start_date, end_date


class WorkPointViewSet(viewsets.ModelViewSet, UserPermissionMixin):
    queryset = WorkPoint.objects.all()
    serializer_class = WorkPointSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def create_point(self, user, timestamp=None):
        timestamp = timestamp or now()
        last_type = (
            WorkPoint.objects.filter(user=user, timestamp__date=now().date())
            .order_by("-timestamp")
            .first()
        )
        next_type = "in" if not last_type or last_type.type == "out" else "out"
        return WorkPoint.objects.create(user=user, type=next_type, timestamp=timestamp)

    @action(detail=True, methods=["post"], url_path="register-point")
    def register_point(self, request, id=None):
        user = self.get_user(request, id)
        point = self.create_point(user)
        return Response(
            {
                "detail": f"Ponto registrado com sucesso: {point.type}",
                "timestamp": point.timestamp.isoformat(),
                "type": point.type,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="register-point-manual")
    def register_point_manual(self, request, id=None):
        user = self.get_user(request, id)
        timestamp = request.data.get("timestamp")

        if not timestamp:
            return Response(
                {"detail": "Timestamp é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            aware_timestamp = make_aware(
                datetime.fromisoformat(timestamp), pytz.timezone("America/Sao_Paulo")
            )
        except ValueError:
            return Response(
                {"detail": "Timestamp inválido. Use o formato ISO 8601."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        point = self.create_point(user, aware_timestamp)
        return Response(
            {
                "detail": f"Ponto manual registrado com sucesso: {point.type}",
                "timestamp": point.timestamp.isoformat(),
                "type": point.type,
            },
            status=status.HTTP_201_CREATED,
        )


class WorkPointReportView(APIView, UserPermissionMixin, DateValidationMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retorna os registros de pontos e métricas detalhadas para um período."""
        user = self.get_user(request, kwargs.get("id"))
        start_date, end_date = self.get_date_params(request)

        points = WorkPoint.objects.filter(
            user=user, timestamp__date__range=(start_date, end_date)
        ).order_by("timestamp")

        grouped_points = self.group_points_by_date(points, start_date, end_date)
        total_worked, remaining, extra = self.calculate_metrics(user, grouped_points)

        return Response(
            {
                "user": {
                    "id": str(user.id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "start_date": start_date.strftime("%d/%m/%Y"),
                "end_date": end_date.strftime("%d/%m/%Y"),
                "points": grouped_points,
                "total_worked": str(total_worked),
                "remaining_hours": str(remaining),
                "extra_hours": str(extra),
                "is_complete": remaining == timedelta(),
            }
        )

    def get_date_params(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            raise ValueError(
                "Os parâmetros 'start_date' e 'end_date' são obrigatórios."
            )

        return self.validate_date_params(start_date, end_date)

    def group_points_by_date(self, points, start_date, end_date):
        all_dates = [
            (start_date + timedelta(days=i))
            for i in range((end_date - start_date).days + 1)
        ]

        grouped_points = {
            date: [
                {"time": point.timestamp.strftime("%H:%M:%S"), "type": point.type}
                for point in points
                if point.timestamp.date() == date
            ]
            for date in all_dates
        }

        return [
            {
                "date_point": date.strftime("%d/%m/%Y"),
                "weekday": date.strftime("%A").lower(),
                "timestamp": grouped_points.get(date, []),
            }
            for date in all_dates
        ]

    def calculate_metrics(self, user, grouped_points):
        total_worked = calculate_worked_hours(grouped_points)
        remaining = calculate_remaining_hours(
            total_worked, user.work_schedule, grouped_points
        )
        extra = calculate_extra_hours(total_worked, user.work_schedule, grouped_points)
        return total_worked, remaining, extra


class WorkPointPDFReportView(WorkPointReportView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if response.status_code != 200:
            return response

        data = response.data
        html = render_to_string(
            "workpoints/report.html",
            {
                "user": data["user"],
                "start_date": data["start_date"],
                "end_date": data["end_date"],
                "report": self.generate_report(data["points"]),
            },
        )

        pdf_response = HttpResponse(content_type="application/pdf")
        pisa.CreatePDF(html, dest=pdf_response)
        pdf_response["Content-Disposition"] = "attachment; filename=relatorio.pdf"
        return pdf_response

    def generate_report(self, points):
        grouped_points = self.group_points(points)
        self.calculate_total_worked(grouped_points)
        return list(grouped_points.values())

    def group_points(self, points):
        grouped_points = {}
        for point in points:
            date = point["date_point"]
            weekday = point["weekday"]

            if date not in grouped_points:
                grouped_points[date] = {
                    "date": date,
                    "weekday": weekday,
                    "entries": point["timestamp"],
                    "total_worked": None,
                }

        return grouped_points

    def calculate_total_worked(self, grouped_points):
        for date, data in grouped_points.items():
            points_for_day = [
                datetime.strptime(entry["time"], "%H:%M:%S")
                for entry in data["entries"]
            ]

            if len(points_for_day) % 2 == 0:
                total_worked = timedelta()
                for i in range(0, len(points_for_day), 2):
                    total_worked += points_for_day[i + 1] - points_for_day[i]
                data["total_worked"] = str(total_worked)


class DailySummaryView(APIView, UserPermissionMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_user(request, kwargs.get("id"))
        today = now().date()
        points = WorkPoint.objects.filter(user=user, timestamp__date=today).order_by(
            "timestamp"
        )
        work_schedule = getattr(user, "work_schedule", None)

        if not work_schedule:
            return Response(
                {"detail": "Horário de trabalho não definido para o usuário."},
                status=400,
            )

        total_worked = calculate_worked_hours(points)
        remaining = calculate_remaining_hours(total_worked, work_schedule, [today])
        extra = calculate_extra_hours(total_worked, work_schedule, [today])

        return Response(
            {
                "points": [
                    {
                        "timestamp": p.timestamp.isoformat(),
                        "type": p.type,
                        "weekday": p.weekday,
                    }
                    for p in points
                ],
                "total_worked": str(total_worked),
                "remaining_hours": str(remaining),
                "extra_hours": str(extra),
                "is_complete": remaining == timedelta(),
            }
        )
