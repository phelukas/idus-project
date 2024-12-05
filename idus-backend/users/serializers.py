from rest_framework import serializers
from .models import User
from re import sub
from rest_framework.exceptions import ValidationError


def validate_cpf(cpf):
    """Valida o CPF com base nos dígitos verificadores."""
    cpf = "".join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf in (c * 11 for c in "0123456789"):
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
        digito = (soma * 10) % 11
        if digito == 10:
            digito = 0
        if digito != int(cpf[i]):
            return False
    return True


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "cpf",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "role",
            "work_schedule",
            "password",
        ]

    def validate_cpf(self, value):
        """Valida o CPF fornecido."""
        if not validate_cpf(value):
            raise ValidationError("O CPF fornecido é inválido.")
        return value

    def create(self, validated_data):
        validated_data["cpf"] = sub(r"[^\d]", "", validated_data["cpf"])

        is_superuser = validated_data.get("role") == "admin"

        user = User.objects.create_user(
            cpf=validated_data["cpf"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            birth_date=validated_data.get("birth_date"),
            password=validated_data["password"],
            role=validated_data.get("role", "common"),
            work_schedule=validated_data.get("work_schedule"),
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
        return user


class UserSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "cpf",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "role",
            "work_schedule",
        ]
