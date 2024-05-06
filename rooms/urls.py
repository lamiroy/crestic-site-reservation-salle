from django.urls import path

from .views import HomePageView, RoomListView, default_image

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('rooms/list/', RoomListView.as_view(), name='roomreservation_list'),
    path('default_image', default_image, name='default_image')
]
