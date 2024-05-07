from django.http import HttpResponse  # Importe la classe HttpResponse pour gérer les réponses HTTP
from django.views.generic import ListView  # Importe la classe ListView pour afficher une liste d'objets
from django.urls import reverse_lazy  # Importe la fonction reverse_lazy pour les URL asynchrones
from hotel_reservation_project import settings  # Importe les paramètres du projet
from .models import RoomCategory  # Importe le modèle RoomCategory
from bookedrooms.models import BookedRoom  # Importe le modèle BookedRoom
from bootstrap_datepicker_plus import DatePickerInput, \
    TimePickerInput  # Importe les widgets DatePickerInput et TimePickerInput
from django.contrib.auth.mixins import \
    LoginRequiredMixin  # Importe le mixin LoginRequiredMixin pour les vues basées sur les classes
from django.views.generic.edit import UpdateView, DeleteView, CreateView  # Importe les vues génériques d'édition
from icalendar import Calendar, Event  # Importe les classes pour créer des fichiers .ics
from datetime import datetime, time  # Importe les classes pour manipuler les dates et heures
import os  # Importe le module os pour les opérations sur le système d'exploitation


def add_to_ics(room_category, people_amount, date, start_time, end_time, groups, motif):
    """
    Ajoute un événement au fichier .ics avec les informations spécifiées.
    """
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
    fullcalendar_dir = os.path.join(script_dir, '..', 'fullcalendar')  # Chemin complet du répertoire 'fullcalendar'
    ics_file_path = os.path.join(fullcalendar_dir, 'calendarFiles', 'calendarBookedroom.ics')  # Chemin du fichier .ics

    # Écrire dans le fichier .ics
    with open(ics_file_path, 'ab') as f:
        f.write(cal.to_ical())
        print("Event added to calendar successfully.")


class HomePageView(LoginRequiredMixin, CreateView):
    """
    Affiche la page d'accueil et gère la création de réservations de chambres.
    """
    model = BookedRoom
    template_name = 'home.html'
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif')
    success_url = reverse_lazy('home')
    login_url = 'login'

    def get_form(self):
        """
        Surcharge pour changer les DateFields en widgets DatePicker.
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
        Surcharge pour toujours définir l'utilisateur sur l'utilisateur actuellement connecté.
        """
        user = self.request.user
        form.instance.user = user
        add_to_ics(form.cleaned_data['room_category'],
                   form.cleaned_data['peopleAmount'],
                   form.cleaned_data['date'],
                   form.cleaned_data['startTime'],
                   form.cleaned_data['endTime'],
                   form.cleaned_data['groups'],
                   form.cleaned_data['motif']
                   )
        return super(HomePageView, self).form_valid(form)


def default_image(request):
    """
    Renvoie l'image par défaut.
    """
    default_image_path = os.path.join(settings.MEDIA_IMAGE)  # Chemin absolu vers l'image par défaut

    # Vérifie si l'image par défaut existe
    if os.path.exists(default_image_path):
        with open(default_image_path, 'rb') as f:
            image_content = f.read()  # Lit le contenu de l'image par défaut
        return HttpResponse(image_content, content_type='image/jpeg')  # Renvoie le contenu de l'image en réponse
    else:
        return HttpResponse(status=404)  # Renvoie une réponse 404 si l'image par défaut n'existe pas


class RoomListView(ListView):
    """
    Affiche une liste des catégories de chambres disponibles.
    """
    model = RoomCategory
    template_name = 'roomreservation_list.html'
    login_url = 'login'
