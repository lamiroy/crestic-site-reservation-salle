from django.apps import AppConfig

# Classe de configuration pour l'application Bookedrooms
class BookedroomsConfig(AppConfig):
    # Nom de l'application
    name = 'bookedrooms'

    def ready(self):
        from . import signals
        # Explicitly connect a signal handler.
        # post_save.connect(utils.send_email)
