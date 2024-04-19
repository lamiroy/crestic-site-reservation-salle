from django.contrib import admin

from .models import BookedRoom


class BookRoomsAdmin(admin.ModelAdmin):
    model = BookedRoom
    list_display = ['id', 'date', 'startTime', 'endTime', 'groups', 'status',
                    'user', 'room_category', 'nbr_of_rooms', 'total_cost']
    readonly_fields = ('total_cost',)


admin.site.register(BookedRoom, BookRoomsAdmin)
