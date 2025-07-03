import os
from celery import Celery
from django.conf import settings

# Solución definitiva para el error de mayúsculas
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tim_DB.settings')

app = Celery('Tim_DB')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configuración multi-entorno
if os.environ.get('DJANGO_DEBUG', 'True') == 'True':
    app.conf.broker_transport_options = {
        'data_folder_in': 'celery_data/in',
        'data_folder_out': 'celery_data/out'
    }
else:
    app.conf.broker_url = 'redis://:Switch123@localhost:6379/0'

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)