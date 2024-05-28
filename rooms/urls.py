from django.urls import path  # Import de la fonction path pour définir les URLs
from .views import (
    HomePageView,  # Import de la vue HomePageView pour la page d'accueil
    RoomListView,  # Import de la vue RoomListView pour la liste des salles
    default_room_image  # Import de la vue default_image pour afficher une image par défaut
)

urlpatterns = [
    path('',
         HomePageView.as_view(), name='home'),  # Définit l'URL pour la page d'accueil avec la vue HomePageView
    path('rooms/list/',
         RoomListView.as_view(), name='roomreservation_list'),  # Définit l'URL pour les salles avec la vue RoomListView
    path('default_room_image',
         default_room_image, name='default_room_image')  # Définit l'URL pour l'image par défaut avec la vue default_image
]
