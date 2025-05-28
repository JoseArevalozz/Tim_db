import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tim_DB.settings')

app = Celery('Tim_DB')

# Configuración especial para Windows
if settings.DEBUG:
    app.conf.broker_transport_options = settings.CELERY_BROKER_TRANSPORT_OPTIONS

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()