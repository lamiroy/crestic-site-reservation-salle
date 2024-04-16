from django.contrib import admin

from .models import RoomCategory

class RoomCategoryAdmin(admin.ModelAdmin):
    model = RoomCategory
    list_display = ['nom_de_la_salle', 'description','nombre_de_personnes', 'motif_de_reservation' ]

admin.site.register(RoomCategory, RoomCategoryAdmin)
