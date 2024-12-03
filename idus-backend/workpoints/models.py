import uuid
from django.db import models
from django.conf import settings


class WorkPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=10, choices=[("in", "Entrada"), ("out", "Saída")]
    )

    def __str__(self):
        return f"{self.user.username} - {self.type} em {self.timestamp}"
