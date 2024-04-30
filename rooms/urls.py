from django.urls import path

from .views import RoomListView

urlpatterns = [
    path('rooms/list/', RoomListView.as_view(), name='roomreservation_list')
]
