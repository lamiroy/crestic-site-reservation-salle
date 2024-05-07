from django.urls import path  # Import de la fonction path pour définir les URL
from .views import (  # Import des vues associées aux URL
    BookedRoomsListView,  # Vue pour afficher la liste des réservations de salles
    BookedRoomsDetailView,  # Vue pour afficher les détails d'une réservation de salle
    BookedRoomsUpdateView,  # Vue pour mettre à jour une réservation de salle
    BookedRoomsDeleteView,  # Vue pour supprimer une réservation de salle
    BookedRoomsCreateView,  # Vue pour créer une nouvelle réservation de salle
)

urlpatterns = [
    path('<int:pk>/edit/',  # URL pour mettre à jour une réservation de salle avec un identifiant spécifique
         BookedRoomsUpdateView.as_view(),  # Utilisation de la vue BookedRoomsUpdateView pour cette URL
         name='bookedrooms_edit'),  # Nom de l'URL pour référence dans le code Django

    path('<int:pk>/',  # URL pour afficher les détails d'une réservation de salle avec un identifiant spécifique
         BookedRoomsDetailView.as_view(),  # Utilisation de la vue BookedRoomsDetailView pour cette URL
         name='bookedrooms_detail'),  # Nom de l'URL pour référence dans le code Django

    path('<int:pk>/delete/',  # URL pour supprimer une réservation de salle avec un identifiant spécifique
         BookedRoomsDeleteView.as_view(),  # Utilisation de la vue BookedRoomsDeleteView pour cette URL
         name='bookedrooms_delete'),  # Nom de l'URL pour référence dans le code Django

    path('new/<int:room_pk>/',  # URL pour créer une nouvelle réservation de salle avec un identifiant de salle spécifique
         BookedRoomsCreateView.as_view(),  # Utilisation de la vue BookedRoomsCreateView pour cette URL
         name='bookedrooms_new'),  # Nom de l'URL pour référence dans le code Django

    path('',  # URL pour afficher la liste des réservations de salles
         BookedRoomsListView.as_view(),  # Utilisation de la vue BookedRoomsListView pour cette URL
         name='bookedrooms_list'),  # Nom de l'URL pour référence dans le code Django
]
