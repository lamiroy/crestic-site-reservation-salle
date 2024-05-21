from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.mixins import (
    LoginRequiredMixin,  # Mélange pour exiger une connexion utilisateur
    UserPassesTestMixin  # Mélange pour vérifier une condition personnalisée
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from rooms.models import RoomCategory  # Import du modèle de catégorie de salle
from bookedrooms.models import BookedRoom  # Import du modèle de réservation de salle


class RoomDashboardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vue pour afficher la liste des salles dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = RoomCategory  # Modèle utilisé pour cette vue
    template_name = 'roomdashboard_list.html'  # Nom du modèle de template utilisé
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser or self.request.user.isSecretary


class RoomDashboardDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Vue pour afficher les détails d'une salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = RoomCategory  # Modèle utilisé pour cette vue
    template_name = 'roomdashboard_detail.html'  # Nom du modèle de template utilisé
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        """
        Ajoute des données supplémentaires au contexte de la vue.
        """
        context = super().get_context_data(**kwargs)
        context['BookedRoom'] = BookedRoom.objects.all()  # Ajouter les objets d'un autre modèle
        return context


class RoomDashboardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue pour mettre à jour les détails d'une salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = RoomCategory  # Modèle utilisé pour cette vue
    fields = ('libRoom', 'description', 'image', 'maxCapacity')  # Champs à afficher dans le formulaire
    template_name = 'roomdashboard_edit.html'  # Nom du modèle de template utilisé
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def get_form(self):
        """
        Surcharge de la méthode pour personnaliser le formulaire.
        """
        form = super(RoomDashboardUpdateView, self).get_form()
        form.fields['libRoom'].label = 'Nom de la salle'
        form.fields['description'].label = 'Description'
        form.fields['image'].label = 'Image'
        form.fields['maxCapacity'].label = 'Nombre de pers. max.'
        form.fields['maxCapacity'].widget.attrs['min'] = 1
        form.fields['maxCapacity'].widget.attrs['max'] = 30
        return form

    def form_valid(self, form):
        """
        Surcharge de la méthode pour traiter le formulaire valide.
        """
        user = self.request.user
        form.instance.user = user
        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(RoomDashboardUpdateView, self).form_valid(form)

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser


class RoomDashboardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vue pour supprimer une salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = RoomCategory  # Modèle utilisé pour cette vue
    template_name = 'roomdashboard_delete.html'  # Nom du modèle de template utilisé
    success_url = reverse_lazy('roomdashboard_list')  # URL de redirection après la suppression
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser


class RoomDashboardCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vue pour créer une nouvelle salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = RoomCategory  # Modèle utilisé pour cette vue
    fields = ('libRoom', 'description', 'image', 'maxCapacity')  # Champs à afficher dans le formulaire
    template_name = 'roomdashboard_new.html'  # Nom du modèle de template utilisé
    success_url = reverse_lazy('roomdashboard_list')  # URL de redirection après la création
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def get_form(self):
        """
        Surcharge de la méthode pour personnaliser le formulaire.
        """
        form = super(RoomDashboardCreateView, self).get_form()
        form.fields['libRoom'].label = 'Nom de la salle'
        form.fields['description'].label = 'Description'
        form.fields['image'].label = 'Image'
        form.fields['maxCapacity'].label = 'Nombre de pers. max.'
        form.fields['maxCapacity'].widget.attrs['min'] = 1
        form.fields['maxCapacity'].widget.attrs['max'] = 30
        return form

    def form_valid(self, form):
        """
        Surcharge de la méthode pour traiter le formulaire valide.
        """
        user = self.request.user
        form.instance.user = user
        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(RoomDashboardCreateView, self).form_valid(form)

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser


class BookedRoomDashboardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vue pour afficher la liste des réservations de salles dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = BookedRoom  # Modèle utilisé pour cette vue
    template_name = 'bookedroomdashboard_list.html'  # Nom du modèle de template utilisé
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser
