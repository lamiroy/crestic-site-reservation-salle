from django.urls import reverse_lazy  # Importe la fonction reverse_lazy pour les redirections différées
from django.views.generic import (
    CreateView,  # Importe la vue générique CreateView
    ListView,  # Importe la vue générique ListView
)
from bookedequipments.models import BookedEquipment
from bookedrooms.models import BookedRoom  # Importe le modèle BookedRoom du package bookedrooms
from .forms import CustomUserCreationForm  # Importe le formulaire CustomUserCreationForm du package actuel


class SignUpView(CreateView):
    """
    View pour l'inscription des utilisateurs.
    Utilise CustomUserCreationForm pour le formulaire.
    Redirige vers la page de connexion une fois l'inscription réussie.
    """
    form_class = CustomUserCreationForm  # Utilise CustomUserCreationForm pour le formulaire d'inscription
    success_url = reverse_lazy('login')  # Redirection vers la page de connexion
    template_name = 'registration/signup.html'  # Template utilisé pour l'inscription


class MyProfileView(ListView):
    """
    View pour afficher le profil de l'utilisateur.
    Affiche les réservations faites par l'utilisateur.
    Utilise le modèle BookedRoom pour récupérer les réservations.
    """
    template_name = 'registration/myprofile_view.html'  # Template utilisé pour afficher le profil
    model = BookedRoom  # Modèle utilisé pour récupérer les réservations

    def get_context_data(self, **kwargs):
        """
        Ajoute des données supplémentaires au contexte de la vue.
        """
        context = super().get_context_data(**kwargs)
        context['BookedEquipment'] = BookedEquipment.objects.all()  # Ajouter les objets d'un autre modèle

        return context
