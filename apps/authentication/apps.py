from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        from . import signals_handlers
        from . import notifications
        super().ready()

