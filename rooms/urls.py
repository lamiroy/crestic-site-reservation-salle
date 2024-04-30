from django.urls import path

from .views import HomePageView, RoomListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('rooms/list/', RoomListView.as_view(), name='roomreservation_list')
]
