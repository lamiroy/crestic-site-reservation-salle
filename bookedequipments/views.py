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
from .models import BookedEquipment


class BookedEquipmentsUpdateView(LoginRequiredMixin, UpdateView):
    model = BookedEquipment
    fields = ('equipment_category', 'date', 'startTime', 'endTime', 'groups', 'motif')
    template_name = 'bookedequipment_edit.html'
    success_url = reverse_lazy('home')
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
        user = self.request.user
        form.instance.user = user
        form.instance.status = BookedEquipment.STATUS_CHOICES[0][0]
        return super(BookedEquipmentsUpdateView, self).form_valid(form)


class BookedEquipmentsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedEquipment
    template_name = 'bookedequipment_delete.html'
    success_url = reverse_lazy('home')
    login_url = 'login'


class BookedEquipmentsCreateView(LoginRequiredMixin, CreateView):
    model = BookedEquipment
    fields = ('equipment_category', 'date', 'startTime', 'endTime', 'groups', 'motif')
    template_name = 'bookedequipment_add.html'
    success_url = reverse_lazy('home')
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
        form = super(BookedEquipmentsCreateView, self).get_form()
        form.fields['equipment_category'].label = 'Nom de l\'équipment'
        form.fields['date'].label = 'Jour de la réservation'
        form.fields['startTime'].label = 'Début de la réservation'
        form.fields['endTime'].label = 'Fin de la réservation'
        form.fields['groups'].label = 'Laboratoire'
        form.fields['motif'].label = 'Motif'
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        return form

    def form_valid(self, form):
        """
        Overridden to always set the user to the currently logged-in user
        """
        user = self.request.user
        form.instance.equipment_category = self.equipment_category
        form.instance.user = user
        form.instance.status = BookedEquipment.STATUS_CHOICES[0][0]

        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(BookedEquipmentsCreateView, self).form_valid(form)


class BookedEquipmentsValidationView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BookedEquipment  # Utilisation du modèle BookedRoom pour cette vue
    template_name = 'bookedequipment_validation.html'
    success_url = reverse_lazy('bookedequipments_validation')
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

    return render(request, 'bookedequipment_validation_refused.html', {'reservation': reservation})


def BookedEquipmentsValidationValidatedView(request, pk):
    # Vérifie si l'utilisateur est authentifié et s'il a les droits nécessaires (secrétaire ou superutilisateur)
    if not request.user.is_authenticated or (not request.user.isSecretary and not request.user.is_superuser):
        raise PermissionDenied

    # Récupère la réservation de salle avec l'identifiant donné ou lève une erreur 404 si non trouvée
    reservation = get_object_or_404(BookedEquipment, id=pk)
    if request.method == 'POST':
        reservation.status = 'validated'  # Met à jour le statut de la réservation à 'validée'
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

    return render(request, 'bookedequipment_validation_validated.html', {'reservation': reservation})
