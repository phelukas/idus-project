# Generated by Django 5.1.3 on 2024-12-06 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workpoints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workpoint',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
