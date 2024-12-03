from rest_framework import serializers
from .models import User
from re import sub


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

    def create(self, validated_data):
        validated_data["cpf"] = sub(r"[^\d]", "", validated_data["cpf"])
        user = User.objects.create_user(
            cpf=validated_data["cpf"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            birth_date=validated_data.get("birth_date"),
            password=validated_data["password"],
            role=validated_data.get("role", "common"),
            work_schedule=validated_data.get("work_schedule"),
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
