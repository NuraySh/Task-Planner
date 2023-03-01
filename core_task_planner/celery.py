import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core_task_planner.settings")
app = Celery("core_task_planner")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()