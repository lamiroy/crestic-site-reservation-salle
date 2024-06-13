from django.urls import path  # Import de la fonction path pour définir les URL
from .views import (
    BookedRoomsUpdateView,  # Vue pour mettre à jour une réservation de salle
    BookedRoomsDeleteView,  # Vue pour supprimer une réservation de salle
    BookedRoomsCreateView,  # Vue pour créer une nouvelle réservation de salle
    BookedRoomsValidationView,  # Vue pour valider une réservation de salle
    BookedRoomsValidationRefusedView,  # Vue pour refuser la validation d'une réservation de salle
    BookedRoomsValidationValidatedView  # Vue pour confirmer la validation d'une réservation de salle
)

urlpatterns = [
    # URL pour mettre à jour une réservation de salle avec un identifiant spécifique
    path('<int:pk>/edit/',
         BookedRoomsUpdateView.as_view(), name='bookedrooms_edit'),
    # URL pour supprimer une réservation de salle avec un identifiant spécifique
    path('<int:pk>/delete/',
         BookedRoomsDeleteView.as_view(), name='bookedrooms_delete'),
    # URL pour créer une nouvelle réservation de salle avec un identifiant de salle spécifique
    path('new/<int:room_pk>/',
         BookedRoomsCreateView.as_view(), name='bookedrooms_new'),
    # URL pour afficher la page de validation d'une réservation
    path('bookedrooms_validation/',
         BookedRoomsValidationView.as_view(), name='bookedrooms_validation'),
    # URL pour supprimer une réservation de salle avec un identifiant spécifique
    path('<int:pk>/delete_request/',
         BookedRoomsValidationRefusedView, name='bookedrooms_validation_refused'),
    # URL pour supprimer une réservation de salle avec un identifiant spécifique
    path('<int:pk>/validate_request/',
         BookedRoomsValidationValidatedView, name='bookedrooms_validation_validated'),
]
