from django.contrib.auth.forms import (
    UserCreationForm,  # Importe le formulaire Django pour la création d'un utilisateur
    UserChangeForm,  # Importe le formulaire Django pour la modification d'un utilisateur
)
from .models import CustomUser  # Importe le modèle CustomUser défini dans le même package



class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire de création d'utilisateur personnalisé.
    """

    class Meta(UserCreationForm.Meta):
        # Utilisation du modèle CustomUser
        model = CustomUser
        # Définition des champs à afficher dans le formulaire de création
        fields = ('first_name', 'last_name', 'username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    """
    Formulaire de modification d'utilisateur personnalisé.
    """

    class Meta:
        # Utilisation du modèle CustomUser
        model = CustomUser
        # Définition des champs à afficher dans le formulaire de modification
        fields = ('first_name', 'last_name', 'username', 'email',)
