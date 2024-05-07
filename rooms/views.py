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


def add_to_ics():
    objets = BookedRoom.objects.all()
    # print('affichage des reservations (brut) :')
    # # Affichez les données
    # for objet in objets:
    #     print(objet.__dict__)

    # for objet in objets:
    #     print('===============================')
    #     print('     Affichage des salles :')
    #     print('===============================')
    #     print('     affichage de l\'id :\n' + '     ' + str(objet.id))
    #     print('     affichage du labo :\n' + '     ' + str(objet.groups))
    #     print('     affichage de la salle :\n' + '     ' + str(objet.room_category))
    #     print('     affichage de la date :\n' + '     ' + str(objet.date))
    #     print('     affichage de l\'heure de début:\n' + '     ' + str(objet.startTime))
    #     print('     affichage de l\'heure de fin:\n' + '     ' + str(objet.endTime))
    #     print('     affichage de status:\n' + '     ' + str(objet.status))
    #     print('     affichage du motif:\n' + '     ' + str(objet.motif))
    #     print('     affichage du nombre de personnes:\n' + '     ' + str(objet.peopleAmount))
    #     print('     affichage du user:\n' + '     ' + str(objet.user))

    cal = Calendar()

    for objet in objets:
        event = Event()
        # 20240504T080000
        dateDeb = datetime.combine(objet.date, objet.startTime)
        dateFin = datetime.combine(objet.date, objet.endTime)
        event.add('summary', str(objet.room_category))
        event.add('dtstart', dateDeb)
        event.add('dtend', dateFin)

        cal.add_component(event)

    ical_data = cal.to_ical()
    current_directory = os.path.dirname(__file__)

    # Chemin relatif vers le fichier
    ics_file_path = os.path.join(current_directory, '..', 'fullcalendar', 'calendarFiles', 'calendarBookedroom.ics')

    # Écrire les données dans le fichier
    with open(ics_file_path, 'wb') as f:
        f.write(ical_data)


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
