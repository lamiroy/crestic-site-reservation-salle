from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire de création d'utilisateur personnalisé.
    """
    class Meta(UserCreationForm.Meta):
        # Utilisation du modèle CustomUser
        model = CustomUser
        # Définition des champs à afficher dans le formulaire de création
        fields = ('first_name', 'last_name', 'username', 'email', 'age',)

class CustomUserChangeForm(UserChangeForm):
    """
    Formulaire de modification d'utilisateur personnalisé.
    """
    class Meta:
        # Utilisation du modèle CustomUser
        model = CustomUser
        # Définition des champs à afficher dans le formulaire de modification
        fields = ('first_name', 'last_name', 'username', 'email', 'age',)
