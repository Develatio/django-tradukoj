from django.apps import AppConfig


class TradukojConfig(AppConfig):
    name = 'tradukoj'
    def ready(self):
        from . import signals as _signals
