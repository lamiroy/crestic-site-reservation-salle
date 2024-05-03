from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from rooms.models import RoomCategory
from bookedrooms.models import BookedRoom


class RoomDashboardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RoomCategory
    template_name = 'roomdashboard_list.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


class RoomDashboardDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = RoomCategory
    template_name = 'roomdashboard_detail.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


class RoomDashboardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RoomCategory
    fields = ('libRoom', 'description', 'image', 'maxCapacity')
    template_name = 'roomdashboard_edit.html'
    login_url = 'login'

    def get_form(self):
        """
        Overridden to change the DateFields from text boxes to
        DatePicker widgets
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
        Overridden to always set the user to the currently logged-in user
        """
        user = self.request.user
        form.instance.user = user
        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(RoomDashboardUpdateView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class RoomDashboardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RoomCategory
    template_name = 'roomdashboard_delete.html'
    success_url = reverse_lazy('roomdashboard_list')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser


class RoomDashboardCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = RoomCategory
    fields = ('libRoom', 'description', 'image', 'maxCapacity')
    template_name = 'roomdashboard_new.html'
    success_url = reverse_lazy('roomdashboard_list')
    login_url = 'login'

    def get_form(self):
        """
        Overridden to change the DateFields from text boxes to
        DatePicker widgets
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
        Overridden to always set the user to the currently logged-in user
        """
        user = self.request.user
        form.instance.user = user
        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(RoomDashboardCreateView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class BookedRoomDashboardListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = BookedRoom
    template_name = 'bookedroomdashboard_list.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser
