import uuid
from django.db import models
from django.conf import settings
from django.utils.timezone import localtime, make_aware, is_naive
import locale

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")


class WorkPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    type = models.CharField(
        max_length=10, choices=[("in", "Entrada"), ("out", "Saída")]
    )
    weekday = models.CharField(max_length=20, editable=False)

    def save(self, *args, **kwargs):
        if is_naive(self.timestamp):
            self.timestamp = make_aware(self.timestamp)

        local_timestamp = localtime(self.timestamp)
        self.weekday = local_timestamp.strftime("%A")

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user.username} - {self.type} em {self.timestamp} ({self.weekday})"
        )
