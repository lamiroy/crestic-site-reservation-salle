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
    path('<int:pk>/edit_equipment/',
         BookedEquipmentsUpdateView.as_view(), name='bookedequipment_edit'),
    path('<int:pk>/delete_equipment/',
         BookedEquipmentsDeleteView.as_view(), name='bookedequipment_delete'),
    path('new/<int:equipment_pk>/',
         BookedEquipmentsCreateView.as_view(), name='bookedequipments_new'),
    path('bookedequipment_validation/',
         BookedEquipmentsValidationView.as_view(), name='bookedequipments_validation'),
    path('<int:pk>/delete_request_equipment/',
         BookedEquipmentsValidationRefusedView, name='bookedequipments_validation_refused'),
    path('<int:pk>/validate_request_equipment/',
         BookedEquipmentsValidationValidatedView, name='bookedequipments_validation_validated'),
]
