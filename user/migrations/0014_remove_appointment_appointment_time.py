# Generated by Django 5.0.7 on 2024-08-01 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_appointment_appointment_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_time',
        ),
    ]
