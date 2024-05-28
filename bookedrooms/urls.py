from django.urls import path  # Import de la fonction path pour définir les URL
from .views import (  # Import des vues associées aux URL
    BookedRoomsListView,  # Vue pour afficher la liste des réservations de salles
    BookedRoomsDetailView,  # Vue pour afficher les détails d'une réservation de salle
    BookedRoomsUpdateView,  # Vue pour mettre à jour une réservation de salle
    BookedRoomsDeleteView,  # Vue pour supprimer une réservation de salle
    BookedRoomsCreateView,  # Vue pour créer une nouvelle réservation de salle
    BookedRoomsValidationView,  # Vue pour valider une réservation de salle
    BookedRoomsValidationRefusedView,  # Vue pour refuser la validation d'une réservation de salle
    BookedRoomsValidationValidatedView  # Vue pour confirmer la validation d'une réservation de salle
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

    path('new/<int:room_pk>/',
         # URL pour créer une nouvelle réservation de salle avec un identifiant de salle spécifique
         BookedRoomsCreateView.as_view(),  # Utilisation de la vue BookedRoomsCreateView pour cette URL
         name='bookedrooms_new'),  # Nom de l'URL pour référence dans le code Django

    path('bookedroom_list/',  # URL pour afficher la liste des réservations de salles
         BookedRoomsListView.as_view(),  # Utilisation de la vue BookedRoomsListView pour cette URL
         name='bookedrooms_list'),  # Nom de l'URL pour référence dans le code Django

    path('bookedrooms_validation/',  # URL pour afficher la page de validation d'une réservation
         BookedRoomsValidationView.as_view(),  # Utilisation de la vue BookedRoomsValidationView pour cette URL
         name='bookedrooms_validation'),  # Nom de l'URL pour référence dans le code Django

    path('<int:pk>/delete_request/',  # URL pour supprimer une réservation de salle avec un identifiant spécifique
         BookedRoomsValidationRefusedView,  # Utilisation de la vue BookedRoomsDeleteView pour cette URL
         name='bookedrooms_validation_refused'),  # Nom de l'URL pour référence dans le code Django

    path('<int:pk>/validate_request/',  # URL pour supprimer une réservation de salle avec un identifiant spécifique
         BookedRoomsValidationValidatedView,  # Utilisation de la vue BookedRoomsDeleteView pour cette URL
         name='bookedrooms_validation_validated'),  # Nom de l'URL pour référence dans le code Django
]
