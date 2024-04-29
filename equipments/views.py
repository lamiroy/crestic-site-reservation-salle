from django.views.generic import ListView
from .models import EquipmentCategory


class HomePageView(ListView):
    model = EquipmentCategory
    template_name = 'home.html'
