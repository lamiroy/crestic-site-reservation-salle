from django.contrib import admin
from .models import BookedEquipment


class BookEquipmentsAdmin(admin.ModelAdmin):
    model = BookedEquipment
    list_display = ['id', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif',
                    'user', 'equipment_category', 'peopleAmount']


admin.site.register(BookedEquipment, BookEquipmentsAdmin)
