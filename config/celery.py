import os

from celery import Celery
# import django

# django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.conf.timezone = 'Europe/Kyiv'
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

