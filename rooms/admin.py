from django.contrib import admin  # Import du module admin de Django
from .models import RoomCategory  # Import du modèle RoomCategory


class RoomCategoryAdmin(admin.ModelAdmin):  # Définition du modèle d'administration pour RoomCategory
    model = RoomCategory  # Spécification du modèle associé
    list_display = ['libRoom', 'description',
                    'maxCapacity']  # Liste des champs à afficher dans l'interface d'administration


admin.site.register(RoomCategory, RoomCategoryAdmin)  # Enregistrement du modèle RoomCategory dans l'interface d'admin
