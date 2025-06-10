import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from workpoints.models import WorkPoint
from workpoints.views import WorkPointViewSet
from workpoints.utils import calculate_worked_hours

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
        f"/api/users/{user.id}/workpoints/register-point-manual/",
        {"timestamp": invalid_timestamp},
        format="json",
    )
    assert response.status_code == 400
    assert "Timestamp inválido" in response.json()["detail"]


def test_register_point_manual_timezone_aware(db, user, client):
    client.force_authenticate(user)
    aware_timestamp = "2024-11-29T09:00:00-03:00"

    response = client.post(
        f"/api/workpoints/{user.id}/register-point-manual/",
        {"timestamp": aware_timestamp},
        format="json",
    )

    assert response.status_code == 201
    assert response.json()["timestamp"] == aware_timestamp
    point = WorkPoint.objects.get(user=user)
    tz = timezone.get_current_timezone()
    stored = point.timestamp.astimezone(tz).isoformat()
    assert stored == aware_timestamp


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


def test_workpoint_str_representation(db, user, workpoint_model):
    timestamp = timezone.make_aware(datetime(2024, 11, 29, 8, 0, 0))
    point = workpoint_model.objects.create(user=user, timestamp=timestamp, type="in")

    expected = f"{user.cpf} - in em {point.timestamp} ({point.weekday})"
    assert str(point) == expected


def test_workpoint_naive_timestamp_saved_as_aware(db, user, workpoint_model):
    naive_dt = datetime(2024, 11, 30, 9, 0, 0)
    point = workpoint_model.objects.create(user=user, timestamp=naive_dt, type="in")

    assert not timezone.is_naive(point.timestamp)
    assert point.timestamp.hour == 9


def test_workpoint_preserve_aware_timestamp(db, user, workpoint_model):
    aware_dt = timezone.make_aware(datetime(2024, 11, 30, 10, 0, 0))
    point = workpoint_model.objects.create(user=user, timestamp=aware_dt, type="in")

    assert point.timestamp == aware_dt


def test_calculate_worked_hours_5x1():
    start = datetime(2024, 4, 22).date()
    end = datetime(2024, 4, 28).date()
    points = [
        {
            "date_point": "22/04/2024",
            "timestamp": [
                {"time": "08:00:00", "type": "in"},
                {"time": "12:00:00", "type": "out"},
                {"time": "13:00:00", "type": "in"},
                {"time": "17:00:00", "type": "out"},
            ],
        }
    ]

    total = calculate_worked_hours(points, start, end, "5x1")
    assert total == 44.0


def test_calculate_worked_hours_6x1():
    start = datetime(2024, 4, 22).date()
    end = datetime(2024, 4, 28).date()
    points = [
        {
            "date_point": "22/04/2024",
            "timestamp": [
                {"time": "08:00:00", "type": "in"},
                {"time": "15:20:00", "type": "out"},
            ],
        }
    ]

    total = calculate_worked_hours(points, start, end, "6x1")
    assert total == 44.0


def test_calculate_worked_hours_12x36():
    start = datetime(2024, 4, 22).date()
    end = datetime(2024, 4, 25).date()
    points = [
        {
            "date_point": "22/04/2024",
            "timestamp": [
                {"time": "08:00:00", "type": "in"},
                {"time": "20:00:00", "type": "out"},
            ],
        }
    ]

    total = calculate_worked_hours(points, start, end, "12x36")
    assert total == 24.0


def test_calculate_worked_hours_4h():
    start = datetime(2024, 4, 22).date()
    end = datetime(2024, 4, 23).date()
    points = [
        {
            "date_point": "22/04/2024",
            "timestamp": [
                {"time": "08:00:00", "type": "in"},
                {"time": "12:00:00", "type": "out"},
            ],
        }
    ]

    total = calculate_worked_hours(points, start, end, "4h")
    assert total == 8.0


def test_calculate_worked_hours_6h():
    start = datetime(2024, 4, 22).date()
    end = datetime(2024, 4, 23).date()
    points = [
        {
            "date_point": "22/04/2024",
            "timestamp": [
                {"time": "08:00:00", "type": "in"},
                {"time": "14:00:00", "type": "out"},
            ],
        }
    ]

    total = calculate_worked_hours(points, start, end, "6h")
    assert total == 12.0


# Permissão de acesso via ViewSet
def test_viewset_user_cannot_list_other_users_points(db, client, user, other_user, workpoint_model):
    workpoint_model.objects.create(user=user, timestamp=timezone.now(), type="in")
    workpoint_model.objects.create(user=other_user, timestamp=timezone.now(), type="in")

    client.force_authenticate(user)
    response = client.get("/api/workpoints/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user"] == str(user.id)


def test_viewset_user_cannot_retrieve_other_users_point(db, client, user, other_user, workpoint_model):
    other_point = workpoint_model.objects.create(user=other_user, timestamp=timezone.now(), type="in")

    client.force_authenticate(user)
    response = client.get(f"/api/workpoints/{other_point.id}/")

    assert response.status_code == 404
