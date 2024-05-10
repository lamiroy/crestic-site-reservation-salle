from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView

from bookedrooms.models import BookedRoom
from .forms import CustomUserCreationForm
from .models import CustomUser

class SignUpView(CreateView):
    """
    View pour l'inscription des utilisateurs.
    Utilise CustomUserCreationForm pour le formulaire.
    Redirige vers la page de connexion une fois l'inscription réussie.
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirection vers la page de connexion
    template_name = 'signup.html'  # Template utilisé pour l'inscription

class MyProfileView(ListView):
    """
    View pour afficher le profil de l'utilisateur.
    Affiche les réservations faites par l'utilisateur.
    Utilise le modèle BookedRoom pour récupérer les réservations.
    """
    template_name = 'myprofile_view.html'  # Template utilisé pour afficher le profil
    model = BookedRoom  # Modèle utilisé pour récupérer les réservations
