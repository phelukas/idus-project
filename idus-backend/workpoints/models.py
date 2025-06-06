import uuid
from django.db import models
from django.conf import settings
from django.utils.timezone import localtime, make_aware, is_naive
import locale

try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    # Ignore if the locale is not available (e.g. in CI environments)
    pass


class WorkPoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    type = models.CharField(
        max_length=10, choices=[("in", "Entrada"), ("out", "Saída")]
    )
    weekday = models.CharField(max_length=20, editable=False)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if is_naive(self.timestamp):
            self.timestamp = make_aware(self.timestamp)

        local_timestamp = localtime(self.timestamp)
        self.weekday = local_timestamp.strftime("%A")

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user.cpf} - {self.type} em {self.timestamp} ({self.weekday})"
        )

    class Meta:
        indexes = [models.Index(fields=["user", "timestamp"])]
