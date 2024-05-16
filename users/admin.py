from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Utilisation des formulaires personnalisés pour l'ajout et la modification des utilisateurs
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # Définition des champs à afficher dans la liste des utilisateurs dans l'interface d'administration
    list_display = ['first_name', 'last_name', 'username', 'email', 'is_staff', 'isSecretary']

# Enregistrement du modèle CustomUser avec l'interface d'administration en utilisant le CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
