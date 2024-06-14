from django.contrib import admin
from .models import EquipmentCategory


class EquipmentCategoryAdmin(admin.ModelAdmin):
    model = EquipmentCategory
    list_display = ['libEquipment', 'description']


admin.site.register(EquipmentCategory, EquipmentCategoryAdmin)
