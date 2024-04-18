from django.contrib import admin

from .models import RoomCategory


class RoomCategoryAdmin(admin.ModelAdmin):
    model = RoomCategory
    list_display = ['libRoom', 'maxCapacity']


admin.site.register(RoomCategory, RoomCategoryAdmin)
