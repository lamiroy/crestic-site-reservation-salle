from django.contrib import admin
from .models import BookedEquipment


class BookEquipmentsAdmin(admin.ModelAdmin):
    model = BookedEquipment
    list_display = ['id', 'date', 'startTime', 'endTime', 'status', 'motif',
                    'user', 'equipment_category', 'last_person_modified', 'last_date_modified']


admin.site.register(BookedEquipment, BookEquipmentsAdmin)
