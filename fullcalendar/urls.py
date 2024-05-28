from django.urls import path  # Importe la fonction path pour définir des chemins d'URL
from .views import *  # Importe toutes les fonctions de vue depuis le module actuel

urlpatterns = [
    # URL pour exporter les vacances au format iCalendar
    path('holiday.ics',
         export_holiday_ics, name='holiday.ics'),
    # URL pour exporter les réservations de salles au format iCalendar
    path('bookedrooms.ics',
         export_bookedrooms_ics, name='bookedrooms.ics'),
    # URL pour exporter les données vers Excel
    path('excel',
         export_to_excel, name='excel'),
]
