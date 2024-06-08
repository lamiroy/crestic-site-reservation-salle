from django.urls import path

from .views import (
    BookedEquipmentsListView,
    BookedEquipmentsDetailView,
    BookedEquipmentsUpdateView,
    BookedEquipmentsDeleteView,
    BookedEquipmentsCreateView, BookedEquipmentsValidationView, BookedEquipmentsValidationRefusedView,
    BookedEquipmentsValidationValidatedView,
)

urlpatterns = [
    path('<int:pk>/edit_equipment/',
         BookedEquipmentsUpdateView.as_view(),
         name='bookedequipment_edit'),
    path('<int:pk>/equipment_details',
         BookedEquipmentsDetailView.as_view(),
         name='bookedequipments_detail'),
    path('<int:pk>/delete_equipment/',
         BookedEquipmentsDeleteView.as_view(),
         name='bookedequipment_delete'),
    path('new/<int:equipment_pk>/',
         BookedEquipmentsCreateView.as_view(),
         name='bookedequipments_new'),
    path('bookedequipment_list/',
         BookedEquipmentsListView.as_view(),
         name='bookedequipments_list'),
    path('bookedequipment_validation/',  # URL pour afficher la page de validation d'une réservation
         BookedEquipmentsValidationView.as_view(),  # Utilisation de la vue BookedRoomsValidationView pour cette URL
         name='bookedequipments_validation'),  # Nom de l'URL pour référence dans le code Django

    path('<int:pk>/delete_request_equipment/',  # URL pour supprimer une réservation de salle avec un identifiant spécifique
         BookedEquipmentsValidationRefusedView,  # Utilisation de la vue BookedRoomsDeleteView pour cette URL
         name='bookedequipments_validation_refused'),  # Nom de l'URL pour référence dans le code Django

    path('<int:pk>/validate_request_equipment/',  # URL pour supprimer une réservation de salle avec un identifiant spécifique
         BookedEquipmentsValidationValidatedView,  # Utilisation de la vue BookedRoomsDeleteView pour cette URL
         name='bookedequipments_validation_validated'),
]
