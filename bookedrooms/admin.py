from django.contrib import admin

from .models import BookedRoom


class BookRoomsAdmin(admin.ModelAdmin):
    model = BookedRoom
    list_display = ['id', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif',
                    'user', 'room_category', 'peopleAmount']


admin.site.register(BookedRoom, BookRoomsAdmin)
