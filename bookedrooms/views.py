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
from datetime import datetime, date, time
from django.core.exceptions import ValidationError


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
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'motif')
    template_name = 'bookedroom_edit.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_form(self):
        form = super().get_form()
        form.fields['room_category'].label = 'Nom de la salle'
        form.fields['peopleAmount'].label = 'Nombre de personne'
        form.fields['peopleAmount'].widget.attrs['min'] = 1
        form.fields['peopleAmount'].widget.attrs['max'] = 30
        form.fields['date'].label = 'Jour de la réservation'
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )
        form.fields['startTime'].label = 'Début de la réservation'
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].label = 'Fin de la réservation'
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        form.fields['groups'].label = 'Laboratoire'
        form.fields['motif'].label = 'Motif'
        return form

    def form_valid(self, form):
        form.instance.last_person_modified = self.request.user
        form.instance.last_date_modified = datetime.now()
        current_user = self.request.user

        # Vérifier si l'utilisateur est un secrétaire ou un administrateur
        if not current_user.is_superuser and not current_user.isSecretary:

            if current_user != form.instance.user:
                form.add_error(None, 'Cette réservation ne vous appartient pas. Veuillez revenir à la page d\'accueil')
            # Validation personnalisée
            selected_date = form.cleaned_data['date']
            start_time = form.cleaned_data['startTime']
            end_time = form.cleaned_data['endTime']

            if selected_date < date.today():
                form.add_error('date', 'Vous ne pouvez pas choisir une date antérieure à aujourd\'hui.')

            if start_time < time(8, 0) or start_time > time(18, 0):
                form.add_error('startTime', 'L\'heure de début doit être entre 8h00 et 18h00.')

            if selected_date == date.today():
                current_time = datetime.now().time()
                new_hour = current_time.hour + 1
                new_minute = current_time.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                min_start_time = time(new_hour, new_minute)
                if start_time <= min_start_time:
                    form.add_error('startTime',
                                   'L\'heure de début doit être supérieure à 1h30 de l\'heure actuelle.')

            if end_time < time(8, 0) or end_time > time(18, 0):
                form.add_error('endTime', 'L\'heure de fin doit être entre 8h00 et 18h00.')
            if end_time <= start_time:
                form.add_error('endTime', 'L\'heure de fin doit être supérieure à l\'heure de début.')

            if selected_date.weekday() == 5 and start_time >= time(12, 30):
                form.add_error('startTime', 'Aucune réservation possible le samedi après 12h30.')
            elif selected_date.weekday() == 6:
                form.add_error('date', 'Aucune réservation possible le dimanche.')

            if form.instance.peopleAmount > form.instance.room_category.maxCapacity:
                form.add_error('peopleAmount', 'Le nombre de personnes dépasse la capacité maximale de la salle.')

            existing_bookings = BookedRoom.objects.filter(
                room_category=form.instance.room_category,
                date=selected_date,
                startTime__lt=end_time,
                endTime__gt=start_time,
            ).exclude(status='pending')

            if existing_bookings.exists():
                form.add_error(None,
                               'Une réservation existante avec un statut autre que "pending" occupe déjà cette salle pendant cette période.')

        if form.errors:
            return self.form_invalid(form)

        form.instance.save()
        add_to_ics()
        return super().form_valid(form)


class BookedRoomsCreateView(LoginRequiredMixin, CreateView):
    model = BookedRoom
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'motif')
    template_name = 'bookedroom_add.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        self.room_category = get_object_or_404(RoomCategory, pk=kwargs['room_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['room_category'] = self.room_category
        return initial

    def get_form(self):
        form = super().get_form()
        form.fields['room_category'].label = 'Nom de la salle'
        form.fields['peopleAmount'].label = 'Nombre de pers. au max.'
        form.fields['peopleAmount'].widget.attrs['min'] = 1
        form.fields['peopleAmount'].widget.attrs['max'] = 30
        form.fields['date'].label = 'Date de la réservation'
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )
        form.fields['startTime'].label = 'Heure de début'
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].label = 'Heure de fin'
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        form.fields['groups'].label = 'Laboratoire'
        form.fields['motif'].label = 'Motif'
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room_category = self.room_category
        current_user = self.request.user

        # Vérifier si l'utilisateur est un secrétaire ou un administrateur
        if not current_user.is_superuser and not current_user.isSecretary:

            # Validation personnalisée
            selected_date = form.cleaned_data['date']
            start_time = form.cleaned_data['startTime']
            end_time = form.cleaned_data['endTime']

            if selected_date < date.today():
                form.add_error('date', 'Vous ne pouvez pas choisir une date antérieure à aujourd\'hui.')

            if start_time < time(8, 0) or start_time > time(18, 0):
                form.add_error('startTime', 'L\'heure de début doit être entre 8h00 et 18h00.')

            if selected_date == date.today():
                current_time = datetime.now().time()
                new_hour = current_time.hour + 1
                new_minute = current_time.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                min_start_time = time(new_hour, new_minute)
                if start_time <= min_start_time:
                    form.add_error('startTime', 'L\'heure de début doit être supérieure à 1h30 de l\'heure actuelle.')

            if end_time < time(8, 0) or end_time > time(18, 0):
                form.add_error('endTime', 'L\'heure de fin doit être entre 8h00 et 18h00.')
            if end_time <= start_time:
                form.add_error('endTime', 'L\'heure de fin doit être supérieure à l\'heure de début.')

            if selected_date.weekday() == 5 and start_time >= time(12, 30):
                form.add_error('startTime', 'Aucune réservation possible le samedi après 12h30.')
            elif selected_date.weekday() == 6:
                form.add_error('date', 'Aucune réservation possible le dimanche.')

            if form.instance.peopleAmount > form.instance.room_category.maxCapacity:
                form.add_error('peopleAmount', 'Le nombre de personnes dépasse la capacité maximale de la salle.')

            existing_bookings = BookedRoom.objects.filter(
                room_category=form.instance.room_category,
                date=selected_date,
                startTime__lt=end_time,
                endTime__gt=start_time,
            ).exclude(status='pending')

            if existing_bookings.exists():
                form.add_error(None,
                               'Une réservation existante avec un statut autre que "pending" occupe déjà cette salle pendant cette période.')

        if form.errors:
            return self.form_invalid(form)

        form.instance.save()
        add_to_ics()
        return super().form_valid(form)


class BookedRoomsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedRoom  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedroom_delete.html'  # Utilisation du template 'bookedroom_delete.html'
    success_url = reverse_lazy('home')  # URL à laquelle rediriger après la suppression
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # send_reservation_confirmation_email_admin(self.object)
        response = super().delete(request, *args, **kwargs)

        # Appel de la fonction add_to_ics pour ajouter l'événement à l'ICS
        add_to_ics()

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
