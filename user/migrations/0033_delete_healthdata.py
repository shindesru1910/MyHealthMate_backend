# Generated by Django 5.0.7 on 2024-08-21 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_remove_userprofile_blood_pressure_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HealthData',
        ),
    ]
