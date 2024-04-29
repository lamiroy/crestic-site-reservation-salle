from django.urls import path

from .views import (
    BookedEquipmentsListView,
    BookedEquipmentsDetailView,
    BookedEquipmentsUpdateView,
    BookedEquipmentsDeleteView,
    BookedEquipmentsCreateView,
)

urlpatterns = [
    path('<int:pk>/edit/',
         BookedEquipmentsListView.as_view(),
         name='bookedequipments_edit'),
    path('<int:pk>/',
         BookedEquipmentsDetailView.as_view(),
         name='bookedequipments_detail'),
    path('<int:pk>/delete/',
         BookedEquipmentsUpdateView.as_view(),
         name='bookedequipments_delete'),
    path('new/<int:equimpent_pk>/',
         BookedEquipmentsDeleteView.as_view(),
         name='bookedequipments_new'),
    path('',
         BookedEquipmentsCreateView.as_view(),
         name='bookedequipments_list'),
]
