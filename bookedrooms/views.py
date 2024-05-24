from bootstrap_datepicker_plus import (
    DatePickerInput,  # Import du widget DatePickerInput pour la sélection de dates dans les formulaires
    TimePickerInput  # Import du widget TimePickerInput pour la sélection d'heures dans les formulaires
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,  # Import du mixin LoginRequiredMixin pour obliger l'authentification de l'utilisateur
    UserPassesTestMixin  # Import du mixin UserPassesTestMixin pour vérifier des conditions sur l'utilisateur
)
from django.shortcuts import (
    render,  # Import de la fonction render pour rendre des templates HTML avec un contexte donné
    get_object_or_404,  # Import de la fonction pour obtenir un objet ou renvoyer une erreur 404 s'il n'existe pas
    redirect  # Import de la fonction redirect pour rediriger vers une autre URL
)
from django.urls import \
    reverse_lazy  # Import de la fonction reverse_lazy pour obtenir les URL inversées de manière retardée
from django.views.generic import (
    ListView,  # Import de la vue générique ListView pour afficher une liste d'objets
    DetailView  # Import de la vue générique DetailView pour afficher les détails d'un objet
)
from django.views.generic.edit import (
    UpdateView,  # Import de la vue générique UpdateView pour mettre à jour un objet existant
    DeleteView,  # Import de la vue générique DeleteView pour supprimer un objet existant
    CreateView  # Import de la vue générique CreateView pour créer un nouvel objet
)
from rooms.models import RoomCategory  # Import du modèle RoomCategory pour les catégories de salles
from rooms.views import add_to_ics  # Import de la vue add_to_ics pour ajouter des événements aux calendriers ICS
from .models import BookedRoom  # Import du modèle BookedRoom pour les réservations de salles
from django.core.exceptions import PermissionDenied  # Import de l'exception pour gérer les permissions refusées
from django.db import transaction  # Import du module transaction pour gérer les transactions de la base de données


class BookedRoomsListView(LoginRequiredMixin, ListView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_list.html'  # Utilisation du template 'bookedroom_list.html'
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    # Retourne uniquement les données de l'utilisateur actuellement connecté
    def get_queryset(self):
        return BookedRoom.objects.filter(
            user=self.request.user).order_by('date')


class BookedRoomsDetailView(LoginRequiredMixin, DetailView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_detail.html'  # Utilisation du template 'bookedroom_detail.html'
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés


class BookedRoomsUpdateView(LoginRequiredMixin, UpdateView):
    model = BookedRoom
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups',
              'motif')  # Champs modifiables dans le formulaire
    template_name = 'bookedroom_edit.html'  # Utilisation du template 'bookedroom_edit.html'
    success_url = reverse_lazy('myprofile')  # URL à laquelle rediriger après la modification
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def get_form(self):
        # Personnalisation du formulaire
        form = super(BookedRoomsUpdateView, self).get_form()
        form.fields['room_category'].label = 'Nom de la salle'  # Changement de l'étiquette du champ room_category

        form.fields['peopleAmount'].label = 'Nombre de personne'  # Changement de l'étiquette du champ peopleAmount
        form.fields['peopleAmount'].widget.attrs['min'] = 1  # Définition de la valeur minimale autorisée
        form.fields['peopleAmount'].widget.attrs['max'] = 30  # Définition de la valeur maximale autorisée

        form.fields['date'].label = 'Jour de la réservation'  # Changement de l'étiquette du champ date
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )

        form.fields['startTime'].label = 'Début de la réservation'  # Changement de l'étiquette du champ startTime
        form.fields['startTime'].widget = TimePickerInput().start_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ startTime

        form.fields['endTime'].label = 'Fin de la réservation'  # Changement de l'étiquette du champ endTime
        form.fields['endTime'].widget = TimePickerInput().end_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ endTime

        form.fields['groups'].label = 'Laboratoire'  # Changement de l'étiquette du champ groups

        form.fields['motif'].label = 'Motif'  # Changement de l'étiquette du champ motif

        return form

    def form_valid(self, form):
        # Validation du formulaire
        user = self.request.user
        form.instance.user = user
        data = super(BookedRoomsUpdateView, self).form_valid(form)

        # send_reservation_confirmation_email_admin(form.instance)
        add_to_ics()

        return data


class BookedRoomsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_delete.html'  # Utilisation du template 'bookedroom_delete.html'
    success_url = reverse_lazy('myprofile')  # URL à laquelle rediriger après la suppression
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # send_reservation_confirmation_email_admin(self.object)
        response = super().delete(request, *args, **kwargs)

        # Appel de la fonction add_to_ics pour ajouter l'événement à l'ICS
        add_to_ics()

        return response


class BookedRoomsCreateView(LoginRequiredMixin, CreateView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'status',
              'motif')  # Champs modifiables dans le formulaire
    template_name = 'bookedroom_add.html'  # Utilisation du template 'bookedroom_add.html'
    success_url = reverse_lazy('myprofile')  # URL à laquelle rediriger après la création
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def dispatch(self, request, *args, **kwargs):
        """
        Remplacement pour s'assurer que la clé primaire passée
        existe
        """
        self.room_category = get_object_or_404(RoomCategory, pk=kwargs['room_pk'])

        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Retourne les données initiales à utiliser pour les formulaires sur cette vue.
        """
        initial = super(BookedRoomsCreateView, self).get_initial()
        initial['room_category'] = self.room_category

        return initial

    def get_form(self):
        """
        Remplacement pour changer les champs DateFields des boîtes de texte en
        widgets DatePicker
        """
        form = super(BookedRoomsCreateView, self).get_form()
        form.fields['room_category'].label = 'Nom de la salle'  # Changement de l'étiquette du champ room_category

        form.fields['peopleAmount'].label = 'Nombre de pers. max.'  # Changement de l'étiquette du champ peopleAmount
        form.fields['peopleAmount'].widget.attrs['min'] = 1  # Définition de la valeur minimale autorisée
        form.fields['peopleAmount'].widget.attrs['max'] = 30  # Définition de la valeur maximale autorisée

        form.fields['date'].label = 'Jour de la réservation'  # Changement de l'étiquette du champ date
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )

        form.fields['startTime'].label = 'Début de la réservation'  # Changement de l'étiquette du champ startTime
        form.fields['startTime'].widget = TimePickerInput().start_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ startTime

        form.fields['endTime'].label = 'Fin de la réservation'  # Changement de l'étiquette du champ endTime
        form.fields['endTime'].widget = TimePickerInput().end_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ endTime

        form.fields['groups'].label = 'Laboratoire'  # Changement de l'étiquette du champ groups

        form.fields['motif'].label = 'Motif'  # Changement de l'étiquette du champ motif

        del form.fields['status']  # Suppression du champ status du formulaire

        return form

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.status = BookedRoom.STATUS_CHOICES[0][0]

        response = super(BookedRoomsCreateView, self).form_valid(form)

        add_to_ics()  # Ajoute la réservation au calendrier ICS

        return response


class BookedRoomsValidationView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_validation.html'  # Utilisation du template 'bookedroom_validation.html'
    success_url = reverse_lazy('bookedrooms_validation')
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.isSecretary or self.request.user.is_superuser


def BookedRoomsValidationRefusedView(request, pk):
    # Vérifie si l'utilisateur est authentifié et s'il a les droits nécessaires (secrétaire ou superutilisateur)
    if not request.user.is_authenticated or (not request.user.isSecretary and not request.user.is_superuser):
        raise PermissionDenied

    # Récupère la réservation de salle avec l'identifiant donné ou lève une erreur 404 si non trouvée
    reservation = get_object_or_404(BookedRoom, id=pk)
    if request.method == 'POST':
        reservation.status = 'canceled'  # Met à jour le statut de la réservation à 'annulée'
        reservation.save()  # Sauvegarde les modifications dans la base de données

        add_to_ics()  # Ajoute la réservation au calendrier ICS

        return redirect('bookedrooms_validation')  # redirigez vers une page de succès ou de confirmation

    return render(request, 'bookedroom_validation_refused.html', {'reservation': reservation})


def BookedRoomsValidationValidatedView(request, pk):
    # Vérifie si l'utilisateur est authentifié et s'il a les droits nécessaires (secrétaire ou superutilisateur)
    if not request.user.is_authenticated or (not request.user.isSecretary and not request.user.is_superuser):
        raise PermissionDenied

    # Récupère la réservation de salle avec l'identifiant donné ou lève une erreur 404 si non trouvée
    reservation = get_object_or_404(BookedRoom, id=pk)
    if request.method == 'POST':
        reservation.status = 'validated'  # Met à jour le statut de la réservation à 'validée'
        reservation.save()  # Sauvegarde les modifications dans la base de données

        # Recherche des réservations en attente qui occupent la même salle
        pending_bookings_to_delete = BookedRoom.objects.filter(
            room_category=reservation.room_category,
            date=reservation.date,
            startTime__lt=reservation.endTime,
            endTime__gt=reservation.startTime,
            status='pending'
        )

        # Suppression des réservations en attente trouvées
        with transaction.atomic():
            pending_bookings_to_delete.delete()

        add_to_ics()  # Ajoute la réservation validée au calendrier ICS

        return redirect('bookedrooms_validation')  # redirigez vers une page de succès ou de confirmation

    return render(request, 'bookedroom_validation_validated.html', {'reservation': reservation})
