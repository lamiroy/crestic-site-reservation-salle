from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from equipments.models import EquipmentCategory
from equipments.views import add_to_ics
from generic.roomforms import BookedEquipmentGenericView
from .models import BookedEquipment
from datetime import datetime, date, time


class UserIsOwnerOrAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (request.user == obj.user or request.user.is_superuser or request.user.isSecretary):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BookedEquipmentsUpdateView(LoginRequiredMixin, UserIsOwnerOrAdminMixin, UpdateView):
    model = BookedEquipment
    fields = ('equipment_category', 'date', 'startTime', 'endTime', 'groups', 'motif')
    template_name = 'bookedequipment/bookedequipment_edit.html'
    success_url = reverse_lazy('home_equipment')
    login_url = 'login'

    def get_form(self):
        form = super(BookedEquipmentsUpdateView, self).get_form()
        form.fields['equipment_category'].label = 'Nom de l''équipement'
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
        form.instance.status = 'pending'
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

            existing_bookings = BookedEquipment.objects.filter(
                equipment_category=form.instance.equipment_category,
                date=selected_date,
                startTime__lt=end_time,
                endTime__gt=start_time,
            ).exclude(status='pending').exclude(id=form.instance.id)

            if existing_bookings.exists():
                form.add_error(None, 'Une réservation existante avec un statut autre que "pending" occupe déjà cette '
                                     'salle pendant cette période.')

        if form.errors:
            return self.form_invalid(form)

        form.instance.save()
        add_to_ics()
        return super().form_valid(form)


class BookedEquipmentsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedEquipment
    template_name = 'bookedequipment/bookedequipment_delete.html'
    success_url = reverse_lazy('home_equipment')
    login_url = 'login'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Change le statut à 'canceled' au lieu de supprimer l'objet
        self.object.status = 'canceled'
        self.object.save()

        # Appel de la fonction add_to_ics pour mettre à jour l'événement dans l'ICS
        add_to_ics()

        return redirect(self.success_url)


class BookedEquipmentsCreateView(BookedEquipmentGenericView, LoginRequiredMixin, CreateView):
    model = BookedEquipment
    template_name = 'bookedequipment/bookedequipment_add.html'
    success_url = reverse_lazy('home_equipment')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden to ensure that the primary key passed
        does exist
        """
        self.equipment_category = get_object_or_404(EquipmentCategory, pk=kwargs['equipment_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(BookedEquipmentsCreateView, self).get_initial()
        initial['equipment_category'] = self.equipment_category
        return initial

    def get_form(self):
        """
        Overridden to change the DateFields from text boxes to
        DatePicker widgets
        """
        form = super().get_form()
        return self.form_template(form)

    def form_valid(self, form):
        """
        Overridden to always set the user to the currently logged-in user
        """
        form.instance.user = self.request.user
        form.instance.equipment_category = self.equipment_category

        form = self.form_validation(form, self.request.user)

        form.instance.save()
        add_to_ics()
        return super().form_valid(form)


class BookedEquipmentsValidationView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BookedEquipment  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedequipment/bookedequipment_validation.html'
    success_url = reverse_lazy('home_equipment')
    login_url = 'login'  # URL vers laquelle rediriger les utilisateurs non authentifiés

    def test_func(self):
        """
        Fonction de test pour vérifier si l'utilisateur est un superutilisateur.
        """
        return self.request.user.isSecretary or self.request.user.is_superuser


def BookedEquipmentsValidationRefusedView(request, pk):
    # Vérifie si l'utilisateur est authentifié et s'il a les droits nécessaires (secrétaire ou superutilisateur)
    if not request.user.is_authenticated or (not request.user.isSecretary and not request.user.is_superuser):
        raise PermissionDenied

    # Récupère la réservation d'équipement avec l'identifiant donné ou lève une erreur 404 si non trouvée
    reservation = get_object_or_404(BookedEquipment, id=pk)
    if request.method == 'POST':
        reservation.status = 'canceled'  # Met à jour le statut de la réservation à 'annulée'
        reservation.save()  # Sauvegarde les modifications dans la base de données

        add_to_ics()  # Ajoute la réservation au calendrier ICS

        return redirect('bookedequipments_validation')  # redirigez vers une page de succès ou de confirmation

    return render(request, 'bookedequipment/bookedequipment_validation_refused.html', {'reservation': reservation})


def BookedEquipmentsValidationValidatedView(request, pk):
    # Vérifie si l'utilisateur est authentifié et s'il a les droits nécessaires (secrétaire ou superutilisateur)
    if not request.user.is_authenticated or (not request.user.isSecretary and not request.user.is_superuser):
        raise PermissionDenied

    # Récupère la réservation de salle avec l'identifiant donné ou lève une erreur 404 si non trouvée
    reservation = get_object_or_404(BookedEquipment, id=pk)
    if request.method == 'POST':
        reservation.status = 'loaned'  # Met à jour le statut de la réservation à 'validée'
        reservation.save()  # Sauvegarde les modifications dans la base de données

        # Recherche des réservations en attente qui occupent la même salle
        pending_bookings_to_delete = BookedEquipment.objects.filter(
            equipment_category=reservation.equipment_category,
            date=reservation.date,
            startTime__lt=reservation.endTime,
            endTime__gt=reservation.startTime,
            status='pending'
        )

        # Suppression des réservations en attente trouvées
        with transaction.atomic():
            pending_bookings_to_delete.delete()

        add_to_ics()  # Ajoute la réservation validée au calendrier ICS

        return redirect('bookedequipments_validation')  # redirigez vers une page de succès ou de confirmation

    return render(request, 'bookedequipment/bookedequipment_validation_validated.html', {'reservation': reservation})
