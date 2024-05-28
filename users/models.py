from django.contrib.auth.models import AbstractUser  # Importe la classe pour créer un modèle d'utilisateur personnalisé
from django.db import models  # Importe le module models de Django pour la définition des modèles de base de données



class CustomUser(AbstractUser):
    isSecretary = models.BooleanField(default=False)
