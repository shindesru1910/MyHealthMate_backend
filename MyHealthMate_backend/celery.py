# myproject/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyHealthMate_backend.settings')

app = Celery('MyHealthMate_backend')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Celery Beat schedule configuration
app.conf.beat_schedule = {
    'send-mail-everyday':{
        'task': 'user.tasks.send_mail_func',
        'schedule': crontab(hour=14, minute=50),
    }
}

#for testing
# from datetime import datetime, timedelta
# now = datetime.now() + timedelta(minutes=5)
# app.conf.beat_schedule = {
#     'send-mail-everyday': {
#         'task': 'user.tasks.send_mail_func',
#         'schedule': crontab(hour=now.hour, minute=now.minute),
#     }
# }