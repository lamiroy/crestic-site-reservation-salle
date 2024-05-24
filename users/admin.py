from django.contrib import admin  # Importe le module d'administration de Django
from django.contrib.auth.admin import UserAdmin  # Importe la classe UserAdmin pour personnaliser l'administration
from .forms import (
    CustomUserCreationForm,  # Importe le formulaire personnalisé de création d'un utilisateur
    CustomUserChangeForm,  # Importe le formulaire personnalisé de modification d'un utilisateur
)
from .models import CustomUser  # Importe le modèle CustomUser pour l'administration des utilisateurs


class CustomUserAdmin(UserAdmin):
    # Utilisation des formulaires personnalisés pour l'ajout et la modification des utilisateurs
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'isSecretary')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Définition des champs à afficher dans la liste des utilisateurs dans l'interface d'administration
    list_display = ['username', 'last_name', 'first_name', 'email', 'is_staff', 'isSecretary']


# Enregistrement du modèle CustomUser avec l'interface d'administration en utilisant le CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
