from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from datetime import date, datetime, time

import bookedrooms.models
from rooms.models import RoomCategory
from .models import BookedEquipment


class BookedEquipmentsListView(LoginRequiredMixin, ListView):
    model = BookedEquipment
    template_name = 'bookedequipment_list.html'
    login_url = 'login'

    # Return only the data for the currently logged-in user
    def get_queryset(self):
        return BookedEquipment.objects.filter(
            user=self.request.user).order_by('date')


class BookedEquipmentsDetailView(LoginRequiredMixin, DetailView):
    model = BookedEquipment
    template_name = 'bookedroom_detail.html'
    login_url = 'login'


class BookedEquipmentsUpdateView(LoginRequiredMixin, UpdateView):
    model = BookedEquipment
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'motif')
    template_name = 'bookedroom_edit.html'
    login_url = 'login'

    def get_form(self):
        form = super(BookedEquipmentsUpdateView, self).get_form()
        form.fields['room_category'].label = 'nom de la salle'
        form.fields['peopleAmount'].label = 'nombre de personnes'
        form.fields['date'].label = 'jour de la réservation'
        form.fields['startTime'].label = 'début de la réservation'
        form.fields['endTime'].label = 'fin de la réservation'
        form.fields['groups'].label = 'laboratoire'
        form.fields['motif'].label = 'motif'
        form.fields['date'].widget = DatePickerInput()
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        return form

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.status = bookedrooms.models.BookedRoom.STATUS_CHOICES[0][0]
        return super(BookedEquipmentsUpdateView, self).form_valid(form)


class BookedEquipmentsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedEquipment
    template_name = 'bookedroom_delete.html'
    success_url = reverse_lazy('bookedrooms_list')
    login_url = 'login'


class BookedEquipmentsCreateView(LoginRequiredMixin, CreateView):
    model = BookedEquipment
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif')
    template_name = 'bookedroom_add.html'
    success_url = reverse_lazy('bookedrooms_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden to ensure that the primary key passed
        does exist
        """
        self.room_category = get_object_or_404(RoomCategory, pk=kwargs['room_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(BookedEquipmentsCreateView, self).get_initial()
        initial['room_category'] = self.room_category
        return initial

    def get_form(self):
        """
        Overridden to change the DateFields from text boxes to
        DatePicker widgets
        """
        form = super(BookedEquipmentsCreateView, self).get_form()
        form.fields['room_category'].label = 'nom de la salle'
        form.fields['peopleAmount'].label = 'nombre de personnes'
        form.fields['date'].label = 'jour de la réservation'
        form.fields['startTime'].label = 'début de la réservation'
        form.fields['endTime'].label = 'fin de la réservation'
        form.fields['groups'].label = 'laboratoire'
        form.fields['motif'].label = 'motif'
        form.fields['date'].widget = DatePickerInput()
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        del form.fields['status']
        return form

    def form_valid(self, form):
        """
        Overridden to always set the user to the currently logged-in user
        """
        user = self.request.user
        form.instance.user = user
        form.instance.status = bookedrooms.models.BookedRoom.STATUS_CHOICES[0][0]

        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(BookedEquipmentsCreateView, self).form_valid(form)
