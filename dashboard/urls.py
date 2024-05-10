from django.urls import path
from .views import (
    RoomDashboardListView,  # Vue pour afficher la liste des salles
    RoomDashboardUpdateView,  # Vue pour mettre à jour les détails d'une salle
    RoomDashboardDetailView,  # Vue pour afficher les détails d'une salle
    RoomDashboardDeleteView,  # Vue pour supprimer une salle
    RoomDashboardCreateView,  # Vue pour créer une nouvelle salle
    BookedRoomDashboardListView,  # Vue pour afficher la liste des réservations de salles
)

urlpatterns = [
    # URLs pour les opérations sur les salles
    path('rooms/<int:pk>/edit/',
         RoomDashboardUpdateView.as_view(), name='roomdashboard_edit'),
    path('rooms/<int:pk>/',
         RoomDashboardDetailView.as_view(), name='roomdashboard_detail'),
    path('rooms/<int:pk>/delete/',
         RoomDashboardDeleteView.as_view(), name='roomdashboard_delete'),
    path('rooms/new/',
         RoomDashboardCreateView.as_view(), name='roomdashboard_new'),
    path('rooms/',
         RoomDashboardListView.as_view(), name='roomdashboard_list'),
    # URL pour afficher la liste des réservations de salles
    path('bookedrooms/',
         BookedRoomDashboardListView.as_view(), name='bookedroomdashboard_list'),
]
