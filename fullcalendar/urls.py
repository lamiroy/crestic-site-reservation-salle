from django.urls import path

from .views import export_ics

urlpatterns = [
    path('', export_ics, name='calendar.ics')
    # Autres URLs de votre application...
]
