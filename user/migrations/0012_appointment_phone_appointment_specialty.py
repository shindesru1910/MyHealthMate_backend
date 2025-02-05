# Generated by Django 5.0.7 on 2024-07-31 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_appointment_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='appointment',
            name='specialty',
            field=models.CharField(blank=True, choices=[('scheduled', 'Scheduled'), ('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=10),
        ),
    ]
