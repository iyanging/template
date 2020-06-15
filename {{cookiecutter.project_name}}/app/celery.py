from app.settings import CELERY_BROKER
from celery import Celery

app = Celery("tmp", broker=CELERY_BROKER)
