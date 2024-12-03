from rest_framework import serializers
from .models import WorkPoint


class WorkPointSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format="hex_verbose")
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = WorkPoint
        fields = ["id", "user", "timestamp", "type"]


class WorkPointReportSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(format="hex_verbose")

    class Meta:
        model = WorkPoint
        fields = ["id", "timestamp", "type"]
        read_only_fields = ["id", "timestamp", "type"]
