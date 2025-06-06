import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        cpf="22233344405",
        email="admin@example.com",
        password="password",
        first_name="Admin",
        last_name="User",
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(
        cpf="12345678909",
        email="user@example.com",
        password="password",
        first_name="Normal",
        last_name="User",
    )

@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        cpf="98765432100",
        email="other@example.com",
        password="password",
        first_name="Other",
        last_name="User",
    )

# UserCreateView

def test_create_user(client, admin_user):
    client.force_authenticate(admin_user)
    payload = {
        "cpf": "11144477735",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
        "password": "password",
        "role": "common",
        "scale": "5x1",
    }
    response = client.post("/api/users/create/", payload, format="json")
    assert response.status_code == 201
    assert response.json()["detail"] == "Usuário criado com sucesso."


def test_create_user_forbidden(client, user):
    client.force_authenticate(user)
    payload = {
        "cpf": "88844477735",
        "email": "forbidden@example.com",
        "first_name": "Forbidden",
        "last_name": "User",
        "password": "password",
        "role": "common",
        "scale": "5x1",
    }
    response = client.post("/api/users/create/", payload, format="json")
    assert response.status_code == 403


def test_create_user_unauthenticated(client):
    payload = {
        "cpf": "99944477735",
        "email": "noauth@example.com",
        "first_name": "No",
        "last_name": "Auth",
        "password": "password",
        "role": "common",
        "scale": "5x1",
    }
    response = client.post("/api/users/create/", payload, format="json")
    assert response.status_code == 401

# UserInfoView

def test_info_self(client, user):
    client.force_authenticate(user)
    response = client.get("/api/users/info/")
    assert response.status_code == 200
    assert response.json()["id"] == str(user.id)


def test_info_other_forbidden(client, user, other_user):
    client.force_authenticate(user)
    response = client.get(f"/api/users/info/{other_user.id}/")
    assert response.status_code == 403

# UserListView

def test_list_admin(client, admin_user, user):
    client.force_authenticate(admin_user)
    response = client.get("/api/users/list/")
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 2


def test_list_common(client, user):
    client.force_authenticate(user)
    response = client.get("/api/users/list/")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == str(user.id)

# UserUpdateView

def test_update_self(client, user):
    client.force_authenticate(user)
    response = client.patch(
        f"/api/users/update/{user.id}/",
        {"first_name": "Updated"},
        format="json",
    )
    assert response.status_code == 200
    assert response.json()["data"]["first_name"] == "Updated"


def test_update_other_forbidden(client, user, other_user):
    client.force_authenticate(user)
    response = client.patch(
        f"/api/users/update/{other_user.id}/",
        {"first_name": "Updated"},
        format="json",
    )
    assert response.status_code == 403

# UserDeleteView

def test_delete_user(client, admin_user, user):
    client.force_authenticate(admin_user)
    response = client.delete(f"/api/users/delete/{user.id}/")
    assert response.status_code == 204
    assert User.objects.filter(id=user.id).count() == 0


def test_delete_self(client, user):
    client.force_authenticate(user)
    response = client.delete(f"/api/users/delete/{user.id}/")
    assert response.status_code == 204
    assert User.objects.filter(id=user.id).count() == 0


def test_delete_other_forbidden(client, user, other_user):
    client.force_authenticate(user)
    response = client.delete(f"/api/users/delete/{other_user.id}/")
    assert response.status_code == 403


def test_delete_user_unauthenticated(client, user):
    response = client.delete(f"/api/users/delete/{user.id}/")
    assert response.status_code == 401
