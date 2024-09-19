from django.urls import path

from .views import (
    BookedEquipmentsUpdateView,
    BookedEquipmentsDeleteView,
    BookedEquipmentsCreateView,
    BookedEquipmentsValidationView,
    BookedEquipmentsValidationRefusedView,
    BookedEquipmentsValidationValidatedView,
)

urlpatterns = [
    path('<int:pk>/edit/',
         BookedEquipmentsUpdateView.as_view(), name='bookedequipment_edit'),
    path('<int:pk>/delete/',
         BookedEquipmentsDeleteView.as_view(), name='bookedequipment_delete'),
    path('new/<int:equipment_pk>/',
         BookedEquipmentsCreateView.as_view(), name='bookedequipments_new'),
    path('bookedequipment_validation/',
         BookedEquipmentsValidationView.as_view(), name='bookedequipments_validation'),
    path('<int:pk>/delete_request/',
         BookedEquipmentsValidationRefusedView, name='bookedequipments_validation_refused'),
    path('<int:pk>/validate_request/',
         BookedEquipmentsValidationValidatedView, name='bookedequipments_validation_validated'),
]
