from django.urls import path
from .views import SignUpView, MyProfileView

urlpatterns = [
    # URL pour l'inscription
    path('signup/',
         SignUpView.as_view(), name='signup'),
    # URL pour afficher le profil de l'utilisateur
    path('myprofile/',
         MyProfileView.as_view(), name='myprofile')
]
