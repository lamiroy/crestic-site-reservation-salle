from django.urls import path  # Import de la fonction path pour définir les URL
from .views import (
    RoomDashboardListView,  # Vue pour afficher la liste des salles
    RoomDashboardUpdateView,  # Vue pour mettre à jour les détails d'une salle
    RoomDashboardDetailView,  # Vue pour afficher les détails d'une salle
    RoomDashboardDeleteView,  # Vue pour supprimer une salle
    RoomDashboardCreateView,  # Vue pour créer une nouvelle salle
    EquipmentDashboardUpdateView,
    EquipmentDashboardDetailView,
    EquipmentDashboardDeleteView,
    EquipmentDashboardCreateView,
    EquipmentDashboardListView
)

urlpatterns = [
    # URL pour mettre à jour les détails d'une salle avec l'identifiant pk
    path('rooms/<int:pk>/edit/',
         RoomDashboardUpdateView.as_view(), name='roomdashboard_edit'),
    # URL pour afficher les détails d'une salle avec l'identifiant pk
    path('rooms/<int:pk>/',
         RoomDashboardDetailView.as_view(), name='roomdashboard_detail'),
    # URL pour supprimer une salle avec l'identifiant pk
    path('rooms/<int:pk>/delete/',
         RoomDashboardDeleteView.as_view(), name='roomdashboard_delete'),
    # URL pour créer une nouvelle salle
    path('rooms/new/',
         RoomDashboardCreateView.as_view(), name='roomdashboard_new'),
    # URL pour afficher la liste des salles
    path('rooms/',
         RoomDashboardListView.as_view(), name='roomdashboard_list'),
    # URL pour mettre à jour les détails d'une salle avec l'identifiant pk
    path('equipments/<int:pk>/edit/',
         EquipmentDashboardUpdateView.as_view(), name='equipmentdashboard_edit'),
    # URL pour afficher les détails d'une salle avec l'identifiant pk
    path('equipments/<int:pk>/',
         EquipmentDashboardDetailView.as_view(), name='equipmentdashboard_detail'),
    # URL pour supprimer une salle avec l'identifiant pk
    path('equipments/<int:pk>/delete/',
         EquipmentDashboardDeleteView.as_view(), name='equipmentdashboard_delete'),
    # URL pour créer une nouvelle salle
    path('equipments/new/',
         EquipmentDashboardCreateView.as_view(), name='equipmentdashboard_new'),
    # URL pour afficher la liste des salles
    path('equipments/',
         EquipmentDashboardListView.as_view(), name='equipmentdashboard_list'),
]
