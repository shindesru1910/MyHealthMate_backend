# Generated by Django 5.0.7 on 2024-08-01 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_appointment_phone_appointment_specialty'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointment_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
