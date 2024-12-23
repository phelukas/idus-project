from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import User


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    if not User.objects.filter(cpf="39416362000").exists():
        User.objects.create_superuser(
            cpf="39416362000",
            email="admin.admin@example.com",
            first_name="Admin",
            last_name="User",
            birth_date="1980-01-01",
            password="admin123",
            role="admin"
        )
