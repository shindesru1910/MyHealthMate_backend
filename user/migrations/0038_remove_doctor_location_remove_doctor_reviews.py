# Generated by Django 5.0.7 on 2024-09-11 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0037_remove_doctor_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='location',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='reviews',
        ),
    ]
