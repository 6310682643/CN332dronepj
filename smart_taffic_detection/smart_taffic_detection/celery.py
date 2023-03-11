# django_celery/celery.py


import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_taffic_detection.settings")

app = Celery("smart_taffic_detection")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()