from celery import Celery

from app.settings import CELERY_BROKER

app = Celery("{{cookiecutter.project_name}}", broker=CELERY_BROKER)
