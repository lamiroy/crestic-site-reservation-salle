from django.http import HttpResponse
from django.views.generic import ListView
from django.urls import reverse_lazy

from hotel_reservation_project import settings
from .models import RoomCategory
from bookedrooms.models import BookedRoom
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from icalendar import Calendar, Event
from datetime import datetime, time
import os


def add_to_ics(room_category, people_amount, date, start_time, end_time, groups, motif):
    cal = Calendar()

    # Définir la catégorie de la salle comme le nom de l'événement
    event = Event()
    event.add('summary', room_category)

    # Convertir la date et l'heure en objets datetime
    start_datetime = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)

    event.add('dtstart', start_datetime)
    event.add('dtend', end_datetime)

    # Ajouter les autres informations comme la description de l'événement
    description = f"Nombre de personnes : {people_amount}\nGroupes : {groups}\nMotif : {motif}"
    event.add('description', description)

    cal.add_component(event)

    # Obtenez le chemin absolu du fichier .ics
    script_dir = os.path.dirname(__file__)  # Répertoire du script
    fullcalendar_dir = os.path.join(script_dir, '..', 'fullcalendar')
    ics_file_path = os.path.join(fullcalendar_dir, 'calendarFiles', 'calendarBookedroom.ics')

    # Écrire dans le fichier .ics
    with open(ics_file_path, 'ab') as f:
        f.write(cal.to_ical())
        print("Event added to calendar successfully.")


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
        print("Test:", form.cleaned_data['room_category'])
        add_to_ics(form.cleaned_data['room_category'],
                   form.cleaned_data['peopleAmount'],
                   form.cleaned_data['date'],
                   form.cleaned_data['startTime'],
                   form.cleaned_data['endTime'],
                   form.cleaned_data['groups'],
                   form.cleaned_data['motif']
                   )
        print("Form errors:", form.errors)
        return super(HomePageView, self).form_valid(form)

def default_image(request):
    # Chemin absolu vers l'image par défaut
    default_image_path = os.path.join(settings.MEDIA_IMAGE)

    # Vérifie si l'image par défaut existe
    if os.path.exists(default_image_path):
        # Ouvre et lit le contenu de l'image par défaut
        with open(default_image_path, 'rb') as f:
            image_content = f.read()

        # Renvoie le contenu de l'image en réponse à la requête
        return HttpResponse(image_content, content_type='image/jpeg')
    else:
        # Renvoie une réponse 404 si l'image par défaut n'existe pas
        return HttpResponse(status=404)


class RoomListView(ListView):
    model = RoomCategory
    template_name = 'roomreservation_list.html'
    login_url = 'login'
