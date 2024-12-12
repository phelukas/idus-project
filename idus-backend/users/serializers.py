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
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

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
            "scale",
            "password",
        ]
        read_only_fields = ["work_schedule"] 

    def validate_password(self, value):
        """Permite que o campo senha seja opcional ao atualizar."""
        if value == "":
            return None
        return value

    def validate_cpf(self, value):
        """Valida o CPF fornecido."""
        if not validate_cpf(value):
            raise ValidationError("O CPF fornecido é inválido.")
        return value

    def validate_scale(self, value):
        """Valida a escala fornecida."""
        valid_scales = ["5x1", "6x1", "12x36", "4h", "6h"]
        if value not in valid_scales:
            raise ValidationError(
                f"Escala inválida. Use uma das seguintes: {', '.join(valid_scales)}."
            )
        return value

    def set_work_schedule(self, scale):
        """Define a jornada de trabalho com base na escala."""
        schedules = {
            "5x1": "8h",
            "6x1": "8h",
            "12x36": "12h",
            "4h": "4h",
            "6h": "6h",
        }
        return schedules.get(scale, "8h")

    def create(self, validated_data):
        validated_data["cpf"] = sub(r"[^\d]", "", validated_data["cpf"])
        validated_data["work_schedule"] = self.set_work_schedule(
            validated_data.get("scale")
        )

        is_superuser = validated_data.get("role") == "admin"

        user = User.objects.create_user(
            cpf=validated_data["cpf"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            birth_date=validated_data.get("birth_date"),
            password=validated_data["password"],
            role=validated_data.get("role", "common"),
            work_schedule=validated_data["work_schedule"],
            scale=validated_data.get("scale", "5x1"),
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
        return user

    def update(self, instance, validated_data):
        scale = validated_data.get("scale", instance.scale)
        validated_data["work_schedule"] = self.set_work_schedule(scale)

        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)

        instance.save()
        return instance


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
            "scale",
        ]
