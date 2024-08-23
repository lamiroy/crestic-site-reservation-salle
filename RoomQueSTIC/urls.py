"""hotel_reservation_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # Import du module admin de Django pour l'interface d'administration
from django.conf import settings  # Import des paramètres de configuration de Django
from .settings import production_prefix

from django.urls import (
    path,  # Fonction pour définir des chemins d'URL
    include,  # Fonction pour inclure d'autres fichiers d'URL
    re_path as url,  # Fonction pour inclure d'autres fichiers d'URL
)
from django.conf.urls.static import static  # Import de la fonction static pour servir les fichiers statiques
import django_cas_ng.views

urlpatterns = [
    url(rf'^{production_prefix}', include(
        [ path('admin/', admin.site.urls),  # URL pour accéder à l'interface d'administration
          path('users/', include('users.urls')),  # URL pour les fonctionnalités liées aux utilisateurs
          path('users/', include('django.contrib.auth.urls')),  # URL pour les fonctionnalités d'authentification des users
          path('dashboard/', include('dashboard.urls')),# URL pour le tableau de bord
          path('roombooking/', include('bookedrooms.urls')),  # URL pour la réservation de salles
          path('equipmentbooking/', include('bookedequipments.urls')),  # URL pour la réservation d'équipements
          path('calendar/', include('fullcalendar.urls')),  # URL pour le calendrier
          path('', include('rooms.urls')),  # URL pour les fonctionnalités liées aux salles
          path('equipments/', include('equipments.urls')),
          path('accounts/login', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
          path('accounts/logout', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
        ],
    ))]

if settings.DEBUG:  # Vérifie si le mode DEBUG est activé dans les paramètres de configuration
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
