from django.apps import AppConfig
import os


class LibraryConfig(AppConfig):
    if os.environ.get('RUN_MAIN', None) != 'true':
        default_auto_field = 'django.db.models.BigAutoField'
        def ready(self):
            from EmailSender import updater
            updater.start()
    
    name = 'Library'
