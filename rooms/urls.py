from django.urls import path  # Importe la fonction path pour définir les URLs
from .views import HomePageView, RoomListView, default_image  # Importe les vues nécessaires depuis le module views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  # Définit l'URL pour la page d'accueil avec la vue HomePageView
    path('rooms/list/', RoomListView.as_view(), name='roomreservation_list'),
    # Définit l'URL pour la liste des salles avec la vue RoomListView
    path('default_image', default_image, name='default_image')
    # Définit l'URL pour l'image par défaut avec la vue default_image
]
