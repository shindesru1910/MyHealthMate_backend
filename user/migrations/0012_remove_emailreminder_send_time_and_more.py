# Generated by Django 5.0.6 on 2024-07-31 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_emailreminder_delete_reminder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailreminder',
            name='send_time',
        ),
        migrations.AddField(
            model_name='emailreminder',
            name='reminder_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
