# forms_db/apps.py
import os
from django.apps import AppConfig


class FormsDbConfig(AppConfig):
    name = 'forms_db'
    
    def ready(self):
        # Importa las tareas para que Celery las descubra
        from . import tasks