from django.views.generic import ListView

from .models import RoomCategory


class RoomListView(ListView):
    model = RoomCategory
    template_name = 'roomreservation_list.html'
    login_url = 'login'
