from django.contrib import admin
from .models import EquipmentCategory


class EquipmentCategoryAdmin(admin.ModelAdmin):
    model = EquipmentCategory
    list_display = ['libRoom', 'maxCapacity']


admin.site.register(EquipmentCategory, EquipmentCategoryAdmin)
