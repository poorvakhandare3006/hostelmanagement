from __future__ import absolute_import

import os

from celery import Celery
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostelmanagement.settings')

app = Celery('hostelmanagement')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.timezone = 'Asia/Kolkata'
app.conf.beat_schedule = {
    'send-email-students': {
        'task': 'website.tasks.send_mail_for_students',
        'schedule': crontab(hour=22),
    },
    'send_lecture_email': {
        'task': 'website.tasks.task_send_lecture_email',
        'schedule': 1800,
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


