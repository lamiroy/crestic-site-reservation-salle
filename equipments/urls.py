from django.urls import path
from .views import HomePageViewEquipment, EquipmentListView, default_equipment_image

urlpatterns = [
    path('calendar/', HomePageViewEquipment.as_view(), name='home_equipment'),
    path('equipment/list/',
         EquipmentListView.as_view(), name='equipmentreservation_list'),  # Définit l'URL pour les salles avec la vue RoomListView
    path('default_equipment_image',
         default_equipment_image, name='default_equipment_image')  # Définit l'URL pour l'image par défaut avec la vue default_image
]
