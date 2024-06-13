from django.urls import path
from .views import (
    HomePageViewEquipment,
    EquipmentListView,
    default_equipment_image
)

urlpatterns = [
    # URL pour afficher le calendrier des équipements
    path('calendar/',
         HomePageViewEquipment.as_view(), name='home_equipment'),
    # URL pour afficher la liste des équipements
    path('equipment/list/',
         EquipmentListView.as_view(), name='equipmentreservation_list'),
    # URL pour récupérer l'image par défaut des équipements
    path('default_equipment_image',
         default_equipment_image, name='default_equipment_image')
]
