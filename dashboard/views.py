from django.contrib.auth.mixins import (
    LoginRequiredMixin,  # Mixin pour exiger une connexion utilisateur
    UserPassesTestMixin  # Mixin pour vérifier une condition personnalisée sur l'utilisateur
)
from django.views.generic import (
    ListView,  # Vue générique pour afficher une liste d'objets
    DetailView  # Vue générique pour afficher les détails d'un objet
)
from django.views.generic.edit import (
    UpdateView,  # Vue générique pour mettre à jour un objet existant
    DeleteView,  # Vue générique pour supprimer un objet existant
    CreateView  # Vue générique pour créer un nouvel objet
)
from django.urls import reverse_lazy  # Import de la fonction reverse_lazy pour obtenir les URL inversées
from bookedequipments.models import BookedEquipment
from equipments.models import EquipmentCategory
from rooms.models import RoomCategory  # Import du modèle RoomCategory pour les catégories de salles
from bookedrooms.models import BookedRoom  # Import du modèle BookedRoom pour les réservations de salles


class RoomDashboardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vue pour afficher la liste des salles dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = RoomCategory  # Modèle utilisé pour cette vue
    template_name = 'roomdashbord/roomdashboard_list.html'  # Nom du modèle de template utilisé
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
    template_name = 'roomdashbord/roomdashboard_detail.html'  # Nom du modèle de template utilisé
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
        room = self.object
        booked_rooms = BookedRoom.objects.filter(room_category=room).exclude(status="canceled")
        context['BookedRoom'] = booked_rooms  # Ajouter les objets d'un autre modèle
        context['has_reservations'] = booked_rooms.exists()

        return context


class RoomDashboardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue pour mettre à jour les détails d'une salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = RoomCategory  # Modèle utilisé pour cette vue
    fields = ('libRoom', 'description', 'image', 'maxCapacity')  # Champs à afficher dans le formulaire
    template_name = 'roomdashbord/roomdashboard_edit.html'  # Nom du modèle de template utilisé
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def get_form(self):
        """
        Surcharge de la méthode pour personnaliser le formulaire.
        """
        form = super(RoomDashboardUpdateView, self).get_form()
        form.fields['libRoom'].label = 'Nom de la salle'  # Personnalise l'étiquette du champ 'libRoom'

        form.fields['description'].label = 'Description'  # Personnalise l'étiquette du champ 'description'

        form.fields['image'].label = 'Image'  # Personnalise l'étiquette du champ 'image'

        form.fields['maxCapacity'].label = 'Nombre de pers. max.'  # Personnalise l'étiquette du champ 'maxCapacity'
        form.fields['maxCapacity'].widget.attrs['min'] = 1  # Définit une valeur minimale pour le champ 'maxCapacity'
        form.fields['maxCapacity'].widget.attrs['max'] = 30  # Définit une valeur maximale pour le champ 'maxCapacity'

        return form

    def form_valid(self, form):
        """
        Surcharge de la méthode pour traiter le formulaire valide.
        """
        user = self.request.user  # Récupère l'utilisateur actuel

        form.instance.user = user
        print("Form data:", form.cleaned_data)  # Affiche les données nettoyées du formulaire dans la console
        print("Form errors:", form.errors)  # Affiche les erreurs du formulaire dans la console

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
    template_name = 'roomdashbord/roomdashboard_delete.html'  # Nom du modèle de template utilisé
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
    template_name = 'roomdashbord/roomdashboard_new.html'  # Nom du modèle de template utilisé
    success_url = reverse_lazy('roomdashboard_list')  # URL de redirection après la création
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def get_form(self):
        """
        Surcharge de la méthode pour personnaliser le formulaire.
        """
        form = super(RoomDashboardCreateView, self).get_form()
        form.fields['libRoom'].label = 'Nom de la salle'  # Personnalise l'étiquette du champ 'libRoom'

        form.fields['description'].label = 'Description'  # Personnalise l'étiquette du champ 'description'

        form.fields['image'].label = 'Image'  # Personnalise l'étiquette du champ 'image'

        form.fields['maxCapacity'].label = 'Nombre de pers. max.'  # Personnalise l'étiquette du champ 'maxCapacity'
        form.fields['maxCapacity'].widget.attrs['min'] = 1  # Définit une valeur minimale pour le champ 'maxCapacity'
        form.fields['maxCapacity'].widget.attrs['max'] = 30  # Définit une valeur maximale pour le champ 'maxCapacity'

        return form

    def form_valid(self, form):
        """
        Surcharge de la méthode pour traiter le formulaire valide.
        """
        user = self.request.user  # Récupère l'utilisateur actuel

        form.instance.user = user
        print("Form data:", form.cleaned_data)  # Affiche les données nettoyées du formulaire dans la console
        print("Form errors:", form.errors)  # Affiche les erreurs du formulaire dans la console

        return super(RoomDashboardCreateView, self).form_valid(form)

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser

# ------------------------------------------------------------------------------------------------ #


class EquipmentDashboardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Vue pour afficher la liste des salles dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = EquipmentCategory  # Modèle utilisé pour cette vue
    template_name = 'equipmentdashbord/equipmentdashboard_list.html'  # Nom du modèle de template utilisé
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser or self.request.user.isSecretary


class EquipmentDashboardDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Vue pour afficher les détails d'une salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = EquipmentCategory  # Modèle utilisé pour cette vue
    template_name = 'equipmentdashbord/equipmentdashboard_detail.html'  # Nom du modèle de template utilisé
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
        equipment = self.object
        booked_equipments = BookedEquipment.objects.filter(equipment_category=equipment).exclude(status="canceled")
        context['BookedEquipment'] = booked_equipments  # Ajouter les objets d'un autre modèle
        context['has_reservations'] = booked_equipments.exists()

        return context


class EquipmentDashboardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vue pour mettre à jour les détails d'une salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = EquipmentCategory  # Modèle utilisé pour cette vue
    fields = ('libEquipment', 'description', 'image')  # Champs à afficher dans le formulaire
    template_name = 'equipmentdashbord/equipmentdashboard_edit.html'  # Nom du modèle de template utilisé
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def get_form(self):
        """
        Surcharge de la méthode pour personnaliser le formulaire.
        """
        form = super(EquipmentDashboardUpdateView, self).get_form()
        form.fields['libEquipment'].label = 'Nom de l\'équipement'  # Personnalise l'étiquette du champ 'libRoom'

        form.fields['description'].label = 'Description'  # Personnalise l'étiquette du champ 'description'

        form.fields['image'].label = 'Image'  # Personnalise l'étiquette du champ 'image'

        return form

    def form_valid(self, form):
        """
        Surcharge de la méthode pour traiter le formulaire valide.
        """
        user = self.request.user  # Récupère l'utilisateur actuel

        form.instance.user = user
        print("Form data:", form.cleaned_data)  # Affiche les données nettoyées du formulaire dans la console
        print("Form errors:", form.errors)  # Affiche les erreurs du formulaire dans la console

        return super(EquipmentDashboardUpdateView, self).form_valid(form)

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser


class EquipmentDashboardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vue pour supprimer une salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = EquipmentCategory  # Modèle utilisé pour cette vue
    template_name = 'equipmentdashbord/equipmentdashboard_delete.html'  # Nom du modèle de template utilisé
    success_url = reverse_lazy('equipmentdashboard_list')  # URL de redirection après la suppression
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser


class EquipmentDashboardCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vue pour créer une nouvelle salle dans le tableau de bord.
    Seuls les superutilisateurs peuvent accéder à cette vue.
    """
    model = EquipmentCategory  # Modèle utilisé pour cette vue
    fields = ('libEquipment', 'description', 'image')  # Champs à afficher dans le formulaire
    template_name = 'equipmentdashbord/equipmentdashboard_new.html'  # Nom du modèle de template utilisé
    success_url = reverse_lazy('equipmentdashboard_list')  # URL de redirection après la création
    login_url = 'login'  # URL de connexion pour les utilisateurs non connectés

    def get_form(self):
        """
        Surcharge de la méthode pour personnaliser le formulaire.
        """
        form = super(EquipmentDashboardCreateView, self).get_form()
        form.fields['libEquipment'].label = 'Nom de l\'équipement'  # Personnalise l'étiquette du champ 'libRoom'

        form.fields['description'].label = 'Description'  # Personnalise l'étiquette du champ 'description'

        form.fields['image'].label = 'Image'  # Personnalise l'étiquette du champ 'image'

        return form

    def form_valid(self, form):
        """
        Surcharge de la méthode pour traiter le formulaire valide.
        """
        user = self.request.user  # Récupère l'utilisateur actuel

        form.instance.user = user
        print("Form data:", form.cleaned_data)  # Affiche les données nettoyées du formulaire dans la console
        print("Form errors:", form.errors)  # Affiche les erreurs du formulaire dans la console

        return super(EquipmentDashboardCreateView, self).form_valid(form)

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.is_superuser
