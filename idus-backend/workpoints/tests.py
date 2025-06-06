import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from workpoints.models import WorkPoint
from workpoints.views import WorkPointViewSet

User = get_user_model()


@pytest.fixture
def user(db):
    """
    Fixture para criar um usuário padrão.
    """
    return User.objects.create_user(
        cpf="00000000001",
        email="testuser@example.com",
        password="password",
        work_schedule="8h",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def admin_user(db):
    """
    Fixture para criar um usuário administrador.
    """
    return User.objects.create_superuser(
        cpf="00000000002",
        email="adminuser@example.com",
        password="password",
        first_name="Admin",
        last_name="User",
    )


@pytest.fixture
def other_user(db):
    """
    Fixture para criar outro usuário.
    """
    return User.objects.create_user(
        cpf="00000000003",
        email="otheruser@example.com",
        password="password",
        work_schedule="8h",
        first_name="Other",
        last_name="User",
    )


@pytest.fixture
def workpoint_model():
    """
    Fixture para o modelo WorkPoint.
    """
    return WorkPoint


@pytest.fixture
def client():
    """
    Fixture para um cliente API autenticado.
    """
    return APIClient()


# Testes de Pontos Automáticos
def test_register_point_auto(db, user, workpoint_model):
    viewset = WorkPointViewSet()
    point1 = viewset.create_point(user)
    assert point1.type == "in"

    point2 = viewset.create_point(user)
    assert point2.type == "out"


# Testes de Pontos Manuais
def test_register_point_manual_valid(db, user, workpoint_model):
    valid_timestamp = "2024-11-29T09:00:00"

    point = workpoint_model.objects.create(
        user=user,
        timestamp=timezone.make_aware(datetime.fromisoformat(valid_timestamp)),
        type="in",
    )
    assert point.timestamp.strftime("%Y-%m-%dT%H:%M:%S") == valid_timestamp
    assert point.type == "in"


def test_register_point_manual_invalid(db, user, client):
    client.force_authenticate(user)
    invalid_timestamp = "2024-11-31T09:00:00"

    response = client.post(
        f"/api/workpoints/{user.id}/register-point-manual/",
        {"timestamp": invalid_timestamp},
        format="json",
    )
    assert response.status_code == 400
    assert "Timestamp inválido" in response.json()["detail"]


# Testes de Relatórios
def test_report_no_points(db, client, user):
    client.force_authenticate(user)
    date = "2024-11-29"
    response = client.get(
        f"/api/workpoints/report/{user.id}/?start_date={date}&end_date={date}"
    )
    assert response.status_code == 200
    assert len(response.json()["points"]) == 0


def test_report_with_points(db, client, user, workpoint_model):
    workpoint_model.objects.create(
        user=user,
        timestamp=timezone.make_aware(datetime.fromisoformat("2024-11-29T08:00:00")),
        type="in",
    )
    workpoint_model.objects.create(
        user=user,
        timestamp=timezone.make_aware(datetime.fromisoformat("2024-11-29T18:00:00")),
        type="out",
    )

    client.force_authenticate(user)
    date = "2024-11-29"
    response = client.get(
        f"/api/workpoints/report/{user.id}/?start_date={date}&end_date={date}"
    )
    assert response.status_code == 200
    assert len(response.json()["points"]) == 2
    assert response.json()["points"][0]["type"] == "in"
    assert response.json()["points"][1]["type"] == "out"


# Testes de Resumo Diário
def test_daily_summary_no_points(db, client, user):
    client.force_authenticate(user)
    response = client.get(f"/api/summary/{user.id}/")
    assert response.status_code == 200
    assert response.json()["total_worked"] == "0.0"


def test_daily_summary_with_points(db, client, user, workpoint_model):
    today = timezone.now().replace(hour=8, minute=0, second=0, microsecond=0)
    workpoint_model.objects.create(user=user, timestamp=today, type="in")
    workpoint_model.objects.create(
        user=user,
        timestamp=today + timedelta(hours=4),
        type="out",
    )

    client.force_authenticate(user)
    response = client.get(f"/api/summary/{user.id}/")
    assert response.status_code == 200
    assert response.json()["total_worked"] == "4.0"


# Testes de Permissões
def test_permission_user_access_other_report(db, client, user, other_user):
    client.force_authenticate(user)
    response = client.get(
        f"/api/workpoints/report/{other_user.id}/?start_date=2024-11-29&end_date=2024-11-29"
    )
    assert response.status_code == 403


def test_permission_admin_access_any_report(db, client, admin_user, other_user):
    client.force_authenticate(admin_user)
    response = client.get(
        f"/api/workpoints/report/{other_user.id}/?start_date=2024-11-29&end_date=2024-11-29"
    )
    assert response.status_code == 200
