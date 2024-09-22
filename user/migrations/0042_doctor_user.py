# Generated by Django 5.0.7 on 2024-09-20 08:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0041_user_is_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
