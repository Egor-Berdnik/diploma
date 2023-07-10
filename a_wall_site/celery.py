import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_wall_site.settings")

app = Celery("a_wall_site")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': {
        'task': 'catalog.tasks.test_scheduled_task',
        'schedule': 10.0
    },
}
