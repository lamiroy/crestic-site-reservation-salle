from django.urls import path  # Importe la fonction path pour définir des chemins d'URL
from .views import *  # Importe toutes les fonctions de vue depuis le module actuel

urlpatterns = [  # Liste des URL patterns pour le module
    path('holiday.ics', export_holiday_ics, name='holiday.ics'),
    # Définit le chemin 'holiday.ics' qui pointe vers la fonction export_holiday_ics
    # Le nom de l'URL est 'holiday.ics'
    path('bookedrooms.ics', export_bookedrooms_ics, name='bookedrooms.ics')
    # Définit le chemin 'bookedrooms.ics' qui pointe vers la fonction export_bookedrooms_ics
    # Le nom de l'URL est 'bookedrooms.ics'
]
