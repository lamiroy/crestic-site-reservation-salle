from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import RoomCategory
from bookedrooms.models import BookedRoom
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView


class HomePageView(LoginRequiredMixin, CreateView):
    model = BookedRoom
    template_name = 'home.html'
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif')
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_form(self):
        """
        Overridden to change the DateFields from text boxes to
        DatePicker widgets
        """
        form = super(HomePageView, self).get_form()
        form.fields['room_category'].label = 'Nom de la salle'

        form.fields['peopleAmount'].label = 'Nombre de pers. max.'
        form.fields['peopleAmount'].widget.attrs['min'] = 1
        form.fields['peopleAmount'].widget.attrs['max'] = 30

        form.fields['date'].label = 'Jour de la réservation'
        form.fields['date'].widget = DatePickerInput()

        form.fields['startTime'].label = 'Début de la réservation'
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')

        form.fields['endTime'].label = 'Fin de la réservation'
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')

        form.fields['groups'].label = 'Laboratoire'

        form.fields['motif'].label = 'Motif'

        del form.fields['status']
        return form

    def form_valid(self, form):
        """
        Overridden to always set the user to the currently logged-in user
        """
        user = self.request.user
        form.instance.user = user
        print("Form data:", form.cleaned_data)
        print("Form errors:", form.errors)
        return super(HomePageView, self).form_valid(form)


class RoomListView(ListView):
    model = RoomCategory
    template_name = 'roomreservation_list.html'
    login_url = 'login'
