"""
WSGI config for hotel_reservation_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os  # Import du module os pour interagir avec le système d'exploitation

from django.core.wsgi import get_wsgi_application  # Import de la fonction pour obtenir l'application WSGI Django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_reservation_project.settings')

application = get_wsgi_application()  # Création de l'application WSGI pour le serveur web
