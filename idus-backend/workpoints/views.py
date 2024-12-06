# Imports padrão do Python
from uuid import UUID
from datetime import datetime, timedelta

# Imports do Django
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, now

# Imports de bibliotecas de terceiros
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa
import pytz

# Imports do aplicativo local
from .models import WorkPoint
from .serializers import WorkPointSerializer
from .utils import (
    calculate_completion_time,
    calculate_extra_hours,
    calculate_remaining_hours,
    calculate_worked_hours,
)

User = get_user_model()


class WorkPointPDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request, user_id=None):
        """Helper para verificar permissões e retornar o usuário correto."""
        if user_id:
            if request.user.is_staff or request.user.id == user_id:
                return get_object_or_404(User, id=user_id)
            raise PermissionDenied("Você só pode acessar seus próprios dados.")
        return request.user

    def get(self, request, *args, **kwargs):
        """
        Gera um relatório PDF para os pontos de trabalho do usuário em um período específico.
        """
        user = self.get_user(request, kwargs.get("id"))
        start_date_param = request.query_params.get("start_date")
        end_date_param = request.query_params.get("end_date")

        if not start_date_param or not end_date_param:
            return Response(
                {
                    "detail": "Os parâmetros 'start_date' e 'end_date' são obrigatórios no formato YYYY-MM-DD."
                },
                status=400,
            )

        try:
            start_date = datetime.strptime(start_date_param, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_param, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Formato de data inválido. Use YYYY-MM-DD."},
                status=400,
            )

        if start_date > end_date:
            return Response(
                {"detail": "'start_date' não pode ser maior que 'end_date'."},
                status=400,
            )

        points = WorkPoint.objects.filter(
            user=user, timestamp__date__range=(start_date, end_date)
        ).order_by("timestamp")

        metrics = WorkPointReportView().calculate_report_metrics(points)
        formatted_points = WorkPointReportView().format_points(points)
        context = {
            "user": user,
            "start_date": start_date.strftime("%d/%m/%Y"),
            "end_date": end_date.strftime("%d/%m/%Y"),
            "points": formatted_points,
            **metrics,
        }

        html = render_to_string("workpoints/report.html", context)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f"attachment; filename=relatorio_{user.id}_{start_date_param}_to_{end_date_param}.pdf"
        )

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return Response({"detail": "Erro ao gerar o PDF."}, status=500)
        return response


class WorkPointViewSet(viewsets.ModelViewSet):
    queryset = WorkPoint.objects.all()
    serializer_class = WorkPointSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        """
        Override para buscar WorkPoint por UUID.
        """
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(id=self.kwargs["id"]).first()
        if not obj:
            raise NotFound("Ponto de trabalho não encontrado.")
        return obj

    def get_user(self, request, user_id=None):
        """
        Helper para verificar permissões e retornar o usuário correto.
        """
        if user_id:
            try:
                user_id = UUID(user_id)
            except ValueError:
                raise NotFound("ID inválido.")
            if request.user.is_staff or request.user.id == user_id:
                return get_object_or_404(User, id=user_id)
            raise PermissionDenied("Você não tem permissão para acessar este usuário.")
        return request.user

    def get_last_point_type(self, user, timestamp=None):
        """
        Helper para obter o último tipo de ponto registrado.
        """
        filter_kwargs = {"user": user}
        if timestamp:
            filter_kwargs["timestamp__lte"] = timestamp

        last_point = (
            WorkPoint.objects.filter(**filter_kwargs).order_by("-timestamp").first()
        )
        return last_point.type if last_point else None

    def determine_next_point_type(self, last_type):
        """
        Determina o próximo tipo de ponto (Entrada ou Saída).
        """
        return "in" if last_type == "out" or not last_type else "out"

    def create_point(self, user, timestamp=None):
        """
        Cria um ponto com base no último tipo registrado.
        """
        if timestamp is None:
            timestamp = now()
        last_type = self.get_last_point_type(user, timestamp)
        next_type = self.determine_next_point_type(last_type)
        point = WorkPoint.objects.create(user=user, type=next_type, timestamp=timestamp)
        return point

    def perform_create(self, serializer):
        """
        Lógica de criação para ponto automático.
        """
        user = self.get_user(self.kwargs.get("id"))
        point = self.create_point(user)
        serializer.save(user=user, type=point.type)

    @action(detail=True, methods=["post"], url_path="register-point")
    def register_point(self, request, id=None):
        """
        Registra automaticamente um ponto alternando entre "Entrada" e "Saída".
        """
        user = self.get_user(request, id)
        point = self.create_point(user)
        return Response(
            {
                "detail": f"Ponto registrado com sucesso: {point.type}",
                "timestamp": point.timestamp,
                "type": point.type,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="register-point-manual",
        parser_classes=[JSONParser],
    )
    def register_point_manual(self, request, id=None):
        """
        Registra um ponto manual com data e hora específicas.
        """
        user = self.get_user(request, id)
        timestamp = request.data.get("timestamp")

        if not timestamp:
            return Response(
                {"detail": "Timestamp é obrigatório para registrar ponto manual."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            timestamp = make_aware(
                datetime.fromisoformat(timestamp), pytz.timezone("America/Sao_Paulo")
            )

        except ValueError:
            return Response(
                {
                    "detail": "Timestamp inválido. Use o formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        point = self.create_point(user, timestamp)
        return Response(
            {
                "detail": f"Ponto manual registrado com sucesso: {point.type} em {timestamp.isoformat()}",
                "timestamp": point.timestamp,
                "type": point.type,
            },
            status=status.HTTP_201_CREATED,
        )


class WorkPointReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user(self, request, user_id=None):
        """
        Verifica permissões e retorna o usuário autorizado.
        """
        if user_id:
            if request.user.is_staff or request.user.id == user_id:
                return get_object_or_404(User, id=user_id)
            raise PermissionDenied("Você só pode acessar seus próprios dados.")
        return request.user

    def calculate_report_metrics(self, points):
        """
        Calcula métricas detalhadas para o relatório.
        """
        if not points:
            return {
                "total_worked": "00:00:00",
                "remaining_hours": "00:00:00",
                "extra_hours": "00:00:00",
                "is_complete": False,
                "completion_time": None,
            }

        total_worked = calculate_worked_hours(points)
        user_schedule = points[0].user.work_schedule if points else None
        remaining = calculate_remaining_hours(total_worked, user_schedule)
        extra = calculate_extra_hours(total_worked, user_schedule)
        is_complete = remaining == timedelta()
        completion_time = calculate_completion_time(points, user_schedule)

        return {
            "total_worked": str(total_worked),
            "remaining_hours": str(remaining),
            "extra_hours": str(extra),
            "is_complete": is_complete,
            "completion_time": completion_time.isoformat() if completion_time else None,
        }

    def format_points(self, points):
        """
        Formata os pontos registrados no formato desejado.
        """
        return [
            {
                "timestamp": p.timestamp.strftime("%d/%m/%Y %H:%M:%S"),
                "type": p.type,
            }
            for p in points
        ]

    def get(self, request, *args, **kwargs):
        """
        Retorna os registros de pontos de trabalho e métricas detalhadas para um período específico.
        """
        user = self.get_user(request, kwargs.get("id"))
        start_date_param = request.query_params.get("start_date")
        end_date_param = request.query_params.get("end_date")

        if not start_date_param or not end_date_param:
            return Response(
                {
                    "detail": "Os parâmetros 'start_date' e 'end_date' são obrigatórios no formato YYYY-MM-DD."
                },
                status=400,
            )

        try:
            start_date = datetime.strptime(start_date_param, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_param, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Formato de data inválido. Use YYYY-MM-DD."},
                status=400,
            )

        if start_date > end_date:
            return Response(
                {"detail": "'start_date' não pode ser maior que 'end_date'."},
                status=400,
            )

        points = WorkPoint.objects.filter(
            user=user, timestamp__date__range=(start_date, end_date)
        ).order_by("timestamp")

        metrics = self.calculate_report_metrics(points)
        formatted_points = self.format_points(points)

        return Response(
            {
                "user": {
                    "id": str(user.id),
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                "start_date": start_date.strftime("%d/%m/%Y"),
                "end_date": end_date.strftime("%d/%m/%Y"),
                "points": formatted_points,
                **metrics,
            }
        )


class DailySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retorna o resumo do dia atual do usuário.
        """
        user = (
            get_object_or_404(User, id=kwargs.get("id"))
            if "id" in kwargs
            else request.user
        )
        today = datetime.now().date()

        points = WorkPoint.objects.filter(user=user, timestamp__date=today).order_by(
            "timestamp"
        )
        total_worked = calculate_worked_hours(points)
        remaining = calculate_remaining_hours(total_worked, user.work_schedule)
        extra = calculate_extra_hours(total_worked, user.work_schedule)
        is_complete = remaining == timedelta()
        completion_time = calculate_completion_time(points, user.work_schedule)

        return Response(
            {
                "points": [{"timestamp": p.timestamp, "type": p.type} for p in points],
                "total_worked": str(total_worked),
                "remaining_hours": str(remaining),
                "extra_hours": str(extra),
                "is_complete": is_complete,
                "completion_time": (
                    completion_time.isoformat() if completion_time else None
                ),
            }
        )
