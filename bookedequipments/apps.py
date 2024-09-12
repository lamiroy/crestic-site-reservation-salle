from django.apps import AppConfig


class BookedequipmentsConfig(AppConfig):
    name = 'bookedequipments'

    def ready(self):
        from . import signals
        # Explicitly connect a signal handler.
        # post_save.connect(utils.send_email)
