# Imports padronizados
from uuid import UUID
from datetime import datetime, timedelta

# Imports do Django
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import make_aware

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
        try:
            return UUID(user_id) if not isinstance(user_id, UUID) else user_id
        except ValueError:
            raise NotFound("ID inválido.")


class DateUtilsMixin:
    """Mixin para validações e operações relacionadas a datas."""

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

    def get_date_params(self, request):
        """Obtém os parâmetros de data da query string."""
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            raise ValueError(
                "Os parâmetros 'start_date' e 'end_date' são obrigatórios."
            )

        return self.validate_date_params(start_date, end_date)

    @staticmethod
    def group_points_by_date(points, start_date, end_date):
        """Agrupa pontos por data."""
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


class ReportMixin(DateUtilsMixin):
    """Mixin para geração de relatórios."""

    def calculate_metrics(self, user, grouped_points, start_date, end_date):
        scale = getattr(user, "scale", None)
        if not scale:
            raise ValueError("A escala de trabalho não está definida para o usuário.")

        total_worked = calculate_worked_hours(
            grouped_points, start_date, end_date, scale
        )
        remaining = calculate_remaining_hours(
            total_worked, user.work_schedule, grouped_points
        )
        extra = calculate_extra_hours(total_worked, user.work_schedule, grouped_points)
        return total_worked, remaining, extra


class PointCreationMixin:
    """Mixin to encapsulate the creation of WorkPoint instances."""

    def create_point(self, user, timestamp=None, latitude=None, longitude=None):
        timestamp = timestamp or datetime.now()
        timestamp = timestamp.replace(tzinfo=None, microsecond=timestamp.microsecond)

        last_type = (
            WorkPoint.objects.filter(user=user, timestamp__date=timestamp.date())
            .order_by("-timestamp")
            .first()
        )
        next_type = "in" if not last_type or last_type.type == "out" else "out"
        return WorkPoint.objects.create(
            user=user,
            type=next_type,
            timestamp=timestamp,
            latitude=latitude,
            longitude=longitude,
        )


class WorkPointViewSet(viewsets.ModelViewSet, UserPermissionMixin, PointCreationMixin):
    queryset = WorkPoint.objects.all()
    serializer_class = WorkPointSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        """Restrict queryset to the requesting user unless staff."""
        user = self.request.user
        if user.is_staff:
            return WorkPoint.objects.all()
        return WorkPoint.objects.filter(user=user)


class UserWorkPointView(viewsets.ViewSet, UserPermissionMixin, PointCreationMixin):
    """Endpoints para registro de pontos por usuário."""

    permission_classes = [IsAuthenticated]

    def register_point(self, request, user_id=None):
        user = self.get_user(request, user_id)
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if not latitude or not longitude:
            return Response(
                {"detail": "Latitude e longitude são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        point = self.create_point(user, latitude=latitude, longitude=longitude)
        return Response(
            {
                "detail": f"Ponto registrado com sucesso: {point.type}",
                "timestamp": point.timestamp.isoformat(),
                "type": point.type,
                "latitude": point.latitude,
                "longitude": point.longitude,
            },
            status=status.HTTP_201_CREATED,
        )

    def register_point_manual(self, request, user_id=None):
        user = self.get_user(request, user_id)
        timestamp = request.data.get("timestamp")

        if not timestamp:
            return Response(
                {"detail": "Timestamp é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            parsed_timestamp = datetime.fromisoformat(timestamp)
            if parsed_timestamp.tzinfo is None or parsed_timestamp.tzinfo.utcoffset(parsed_timestamp) is None:
                aware_timestamp = make_aware(
                    parsed_timestamp,
                    pytz.timezone("America/Sao_Paulo"),
                )
            else:
                aware_timestamp = parsed_timestamp
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


class WorkPointReportView(APIView, UserPermissionMixin, ReportMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_user(request, kwargs.get("id"))
        start_date, end_date = self.get_date_params(request)

        points = WorkPoint.objects.filter(
            user=user, timestamp__date__range=(start_date, end_date)
        ).order_by("timestamp")

        total_worked, remaining, extra = self.calculate_metrics(
            user,
            self.group_points_by_date(points, start_date, end_date),
            start_date,
            end_date,
        )

        return Response(
            {
                "user": {
                    "id": str(user.id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "start_date": start_date.strftime("%d/%m/%Y"),
                "end_date": end_date.strftime("%d/%m/%Y"),
                "points": [
                    {
                        "timestamp": p.timestamp.isoformat(),
                        "type": p.type,
                        "weekday": p.timestamp.strftime("%A").lower(),
                    }
                    for p in points
                ],
                "total_worked": str(total_worked),
                "remaining_hours": str(remaining),
                "extra_hours": str(extra),
                "is_complete": remaining == 0,
            }
        )


class WorkPointPDFReportView(WorkPointReportView):
    """Gera um relatório PDF dos pontos registrados."""

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
                "report": data["points"],
            },
        )

        pdf_response = HttpResponse(content_type="application/pdf")
        pisa.CreatePDF(html, dest=pdf_response)
        pdf_response["Content-Disposition"] = "attachment; filename=relatorio.pdf"
        return pdf_response


class DailySummaryView(APIView, UserPermissionMixin, ReportMixin):
    """Exibe um resumo diário dos pontos registrados."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.get_user(request, kwargs.get("id"))
        today = datetime.now().date()

        points = WorkPoint.objects.filter(user=user, timestamp__date=today).order_by(
            "timestamp"
        )
        scale = getattr(user, "scale", None)

        if not scale:
            return Response(
                {"detail": "Escala de trabalho não definida para o usuário."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        grouped_points = self.group_points_by_date(points, today, today)
        total_worked = calculate_worked_hours(
            grouped_points, start_date=today, end_date=today, scale=scale
        )
        remaining = calculate_remaining_hours(
            total_worked, user.work_schedule, grouped_points
        )
        return Response(
            {
                "date": today.strftime("%d/%m/%Y"),
                "points": [
                    {
                        "timestamp": p.timestamp.isoformat(),
                        "type": p.type,
                        "weekday": p.timestamp.strftime("%A").lower(),
                    }
                    for p in points
                ],
                "total_worked": str(total_worked),
                "is_complete": remaining == 0,
            }
        )
