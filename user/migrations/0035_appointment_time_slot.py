# Generated by Django 5.0.7 on 2024-08-24 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_healthdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='time_slot',
            field=models.CharField(blank=True, choices=[('12:00 PM', '12:00 PM'), ('1:00 PM', '1:00 PM'), ('2:00 PM', '2:00 PM'), ('3:00 PM', '3:00 PM'), ('4:00 PM', '4:00 PM'), ('5:00 PM', '5:00 PM')], max_length=10),
        ),
    ]
