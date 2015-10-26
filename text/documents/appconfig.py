from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'documents'
    verbose_name = 'Documents'

    def ready(self):
        # import signal handlers
        from . import signals
