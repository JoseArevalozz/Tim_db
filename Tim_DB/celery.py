import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tim_DB.settings')

app = Celery('Tim_DB')

# Configuración para Windows (local)
if settings.DEBUG:
    app.conf.broker_transport_options = settings.CELERY_BROKER_TRANSPORT_OPTIONS

# Configuración para Linux (producción)
else:
    app.conf.broker_url = 'redis://:Switch123@localhost:6379/0'  # Broker en Redis

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()