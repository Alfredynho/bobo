from django.apps import AppConfig


class MessengerConfig(AppConfig):
    name = 'apps.messenger'

    def ready(self):
        import apps.messenger.signals
