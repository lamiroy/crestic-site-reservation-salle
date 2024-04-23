from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from datetime import date, datetime, time

import bookedrooms.models
from rooms.models import RoomCategory
from .models import BookedRoom


class BookedRoomsListView(LoginRequiredMixin, ListView):
    model = BookedRoom
    template_name = 'bookedroom_list.html'
    login_url = 'login'

    # Return only the data for the currently logged in user
    def get_queryset(self):
        return BookedRoom.objects.filter(
            user=self.request.user).order_by('date')


class BookedRoomsDetailView(LoginRequiredMixin, DetailView):
    model = BookedRoom
    template_name = 'bookedroom_detail.html'
    login_url = 'login'


class BookedRoomsUpdateView(LoginRequiredMixin, UpdateView):
    model = BookedRoom
    fields = ('room_category', 'nbr_of_rooms', 'date', 'startTime', 'endTime', 'groups', 'motif')
    template_name = 'bookedroom_edit.html'
    login_url = 'login'

    def get_form(self):
        form = super(BookedRoomsUpdateView, self).get_form()
        form.fields['date'].widget = DatePickerInput()
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].widget = TimePickerInput().start_of('duration')
        return form

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        form.instance.status = bookedrooms.models.BookedRoom.STATUS_CHOICES[0][0]

        selected_date = form.cleaned_data['date']
        if selected_date < date.today():
            form.add_error('date', 'Vous ne pouvez pas changer la date pour une date antérieure à aujourd\'hui.')
            return self.form_invalid(form)

        start_time = form.cleaned_data.get("startTime")
        if start_time:
            if start_time < time(6, 0) or start_time > time(19, 30):
                form.add_error("startTime", "L'heure de début doit être entre 6h00 et 19h30.")
                return self.form_invalid(form)

            if selected_date == date.today():
                current_time = datetime.now().time()
                new_hour = current_time.hour + 1
                new_minute = current_time.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                min_start_time = time(new_hour, new_minute)
                if start_time <= min_start_time:
                    form.add_error("startTime", "L'heure de début doit être supérieure à 1h30 de l'heure actuelle.")
                    return self.form_invalid(form)

        return super(BookedRoomsUpdateView, self).form_valid(form)


class BookedRoomsDeleteView(LoginRequiredMixin, DeleteView):
    model = BookedRoom
    template_name = 'bookedroom_delete.html'
    success_url = reverse_lazy('bookedrooms_list')
    login_url = 'login'


class BookedRoomsCreateView(LoginRequiredMixin, CreateView):
    model = BookedRoom
    fields = ('room_category', 'nbr_of_rooms', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif')
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
        initial = super(BookedRoomsCreateView, self).get_initial()
        initial['room_category'] = self.room_category
        return initial

    def get_form(self):
        """
        Overridden to change the DateFields from text boxes to
        DatePicker widgets
        """
        form = super(BookedRoomsCreateView, self).get_form()
        form.fields['room_category'].label = 'nom de la salle'
        form.fields['nbr_of_rooms'].label = 'nombre de personnes'
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
        Overridden to always set the user to the currently logged in user
        """
        user = self.request.user
        form.instance.user = user
        form.instance.status = bookedrooms.models.BookedRoom.STATUS_CHOICES[0][0]

        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(BookedRoomsCreateView, self).form_valid(form)
