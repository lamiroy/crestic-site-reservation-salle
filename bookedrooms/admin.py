from django.contrib import admin  # Importation du module d'administration de Django
from .models import BookedRoom  # Import du modèle de réservation de salle


class BookRoomsAdmin(admin.ModelAdmin):
    model = BookedRoom  # Spécification du modèle associé à cette classe d'administration
    # Définition des champs à afficher dans la liste des réservations de salle
    list_display = ['id', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif',
                    'user', 'room_category', 'peopleAmount', 'last_person_modified', 'last_date_modified']


# Enregistrement du modèle BookedRoom avec sa classe d'administration
admin.site.register(BookedRoom, BookRoomsAdmin)
