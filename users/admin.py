from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


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
