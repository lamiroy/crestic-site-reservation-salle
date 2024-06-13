from django.urls import path  # Import de la fonction path pour définir les URLs
from .views import (
    HomePageView,  # Import de la vue HomePageView pour la page d'accueil
    RoomListView,  # Import de la vue RoomListView pour la liste des salles
    default_room_image  # Import de la vue default_image pour afficher une image par défaut
)

urlpatterns = [
    # URL pour afficher le calendrier des salles
    path('',
         HomePageView.as_view(), name='home'),
    # URL pour afficher la liste des salles
    path('rooms/list/',
         RoomListView.as_view(), name='roomreservation_list'),
    # URL pour récupérer l'image par défaut des salles
    path('default_room_image',
         default_room_image, name='default_room_image')
]
