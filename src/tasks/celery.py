from celery import Celery

from config.env import BASE_DIR, env

env.read_env(BASE_DIR / ".env")

app = Celery("tasks")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
