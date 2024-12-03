from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("O CPF é obrigatório.")
        if not email:
            raise ValueError("O email é obrigatório.")

        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuários devem ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuários devem ter is_superuser=True.")

        return self.create_user(cpf, email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    cpf = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[("admin", "Admin"), ("common", "Common")],
        default="common",
    )
    work_schedule = models.CharField(max_length=50, null=True, blank=True, default="8h")

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cpf})"
