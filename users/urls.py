from django.urls import path  # Importe la fonction path pour définir des chemins d'URL
from .views import (
    SignUpView,  # Importe la vue SignUpView du module views du package actuel
    MyProfileView,  # Importe la vue MyProfileView du module views du package actuel
)

urlpatterns = [
    # URL pour l'inscription
    path('signup/',
         SignUpView.as_view(), name='signup'),
    # URL pour afficher le profil de l'utilisateur
    path('myprofile/',
         MyProfileView.as_view(), name='myprofile')
]
