from django.apps import AppConfig
from django.core.signals import post_save

from RoomQueSTIC import utils


# Classe de configuration pour l'application Bookedrooms
class BookedroomsConfig(AppConfig):
    # Nom de l'application
    name = 'bookedrooms'

    def ready(self):

        # Explicitly connect a signal handler.
        post_save.connect(utils.send_email)
