# Generated by Django 5.0.6 on 2024-07-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_reminder_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('send_time', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Reminder',
        ),
    ]
