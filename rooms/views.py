from django.http import HttpResponse  # Importe la classe HttpResponse pour gérer les réponses HTTP
from django.views.generic import ListView  # Importe la classe ListView pour afficher une liste d'objets
from django.urls import reverse_lazy  # Importe la fonction reverse_lazy pour les URL asynchrones
from RoomQueSTIC import settings  # Importe les paramètres du projet
from .models import RoomCategory  # Importe le modèle RoomCategory
from bookedrooms.models import BookedRoom  # Importe le modèle BookedRoom
from bootstrap_datepicker_plus import (
    DatePickerInput,  # Import du widget DatePickerInput de Bootstrap
    TimePickerInput  # Import du widget TimePickerInput de Bootstrap
)
from django.contrib.auth.mixins import \
    LoginRequiredMixin  # Importe le mixin LoginRequiredMixin pour les vues basées sur les classes
from django.views.generic.edit import CreateView  # Import de la classe CreateView pour créer des objets dans une vue
from icalendar import (
    Calendar,  # Import du module Calendar de la bibliothèque iCalendar
    Event  # Import du module Event de la bibliothèque iCalendar
)
from datetime import datetime, date, time  # Import de la classe datetime pour manipuler les dates et heures
import os  # Importe le module os pour les opérations sur le système d'exploitation
import json  # Import du module json pour la manipulation de données JSON

from generic.roomforms import BookedRoomsGenericView

def add_to_ics():
    """
        Ajout des events dans le .ics avec le Json dans le titre
    """
    calWithJson = Calendar()  # Crée un objet iCalendar pour stocker les événements avec les données JSON

    objets = BookedRoom.objects.all()  # Crée un objet iCalendar pour stocker les événements avec les données JSON
    for objet in objets:
        if objet.status != "canceled":
            dateDeb = datetime.combine(objet.date, objet.startTime)  # Combine la date et l'heure de début
            dateFin = datetime.combine(objet.date, objet.endTime)  # Combine la date et l'heure de fin

            # Crée un dictionnaire avec les données à stocker dans le titre
            jsonData = {
                "id": str(objet.id),
                "labo": str(objet.groups),
                "nom": str(objet.room_category),
                "status": str(objet.status),
                "motif": objet.motif,
                "nombre_personnes": str(objet.peopleAmount),
                "max_capacity": str(objet.room_category.maxCapacity),
                "user": str(objet.user),
                "holiday": "false"
            }

            event = Event()  # Crée un nouvel événement iCalendar
            event.add('summary', json.dumps(jsonData))  # Ajoute les données JSON dans le titre de l'événement
            event.add('dtstart', dateDeb)  # Ajoute la date et l'heure de début
            event.add('dtend', dateFin)  # Ajoute la date et l'heure de fin

            calWithJson.add_component(event)  # Ajoute l'événement au calendrier iCalendar

    # Chemin absolu vers le fichier .ics
    ical_data = calWithJson.to_ical()
    current_directory = os.path.dirname(__file__)

    # Chemin relatif vers le fichier
    ics_file_path = os.path.join(current_directory, '..', 'fullcalendar', 'calendarFiles', 'calendarBookedroom.ics')

    # Écrire les données dans le fichier
    with open(ics_file_path, 'wb') as f:
        f.write(ical_data)

    # Ajout des events dans le .ics avec le Json dans le titre
    cal = Calendar()

    for objet in objets:
        dateDeb = datetime.combine(objet.date, objet.startTime)  # Combine la date et l'heure de début
        dateFin = datetime.combine(objet.date, objet.endTime)  # Combine la date et l'heure de fin

        # Crée le titre de l'événement en combinant des informations statiques avec les données de la réservation
        title = 'Salle : ' + str(objet.room_category)
        title += ' Nombre de personnes : ' + str(objet.peopleAmount)
        title += '/' + str(objet.room_category.maxCapacity)
        title += ' Motif : ' + str(objet.motif)
        title += ' Laboratoire : ' + str(objet.groups)
        title += ' Statut : ' + str(objet.status)

        event = Event()  # Crée un nouvel événement iCalendar
        event.add('summary', title)  # Ajoute le titre de l'événement
        event.add('dtstart', dateDeb)  # Ajoute la date et l'heure de début
        event.add('dtend', dateFin)  # Ajoute la date et l'heure de fin

        cal.add_component(event)  # Ajoute l'événement au calendrier iCalendar

    # Chemin absolu vers le fichier .ics
    ical_data = cal.to_ical()
    current_directory = os.path.dirname(__file__)

    # Chemin relatif vers le fichier
    ics_file_path = os.path.join(current_directory, '..', 'fullcalendar', 'calendarFiles', 'calendrier_reservation.ics')

    # Écrire les données dans le fichier
    with open(ics_file_path, 'wb') as f:
        f.write(ical_data)


class HomePageView(BookedRoomsGenericView, LoginRequiredMixin, CreateView):
    """
    Affiche la page d'accueil et gère la création de réservations de chambres.
    """
    model = BookedRoom  # Spécifie le modèle utilisé pour la création d'objets dans la vue
    template_name = 'home.html'  # Spécifie le modèle de template utilisé pour rendre la vue
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'status',
              'motif')  # Spécifie les champs du formulaire
    success_url = reverse_lazy('home')  # Spécifie l'URL de redirection après une soumission réussie du formulaire
    login_url = 'login'  # Spécifie l'URL de connexion pour les utilisateurs non authentifiés

    def get_form(self):
        """
        Surcharge pour changer les DateFields en widgets DatePicker.
        """
        form = super(HomePageView, self).get_form()
        form.fields['room_category'].label = 'Nom de la salle'  # Changement de l'étiquette du champ room_category

        form.fields['peopleAmount'].label = 'Nombre de pers. max.'  # Changement de l'étiquette du champ peopleAmount
        form.fields['peopleAmount'].widget.attrs['min'] = 1  # Définition de la valeur minimale autorisée
        form.fields['peopleAmount'].widget.attrs['max'] = 30  # Définition de la valeur maximale autorisée

        form.fields['date'].label = 'Jour de la réservation'  # Changement de l'étiquette du champ date
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )

        form.fields['startTime'].label = 'Début de la réservation'  # Changement de l'étiquette du champ startTime
        form.fields['startTime'].widget = TimePickerInput().start_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ startTime

        form.fields['endTime'].label = 'Fin de la réservation'  # Changement de l'étiquette du champ endTime
        form.fields['endTime'].widget = TimePickerInput().end_of(
            'duration')  # Utilisation du widget TimePickerInput pour le champ endTime

        form.fields['groups'].label = 'Laboratoire'  # Changement de l'étiquette du champ groups

        form.fields['motif'].label = 'Motif'  # Changement de l'étiquette du champ motif

        del form.fields['status']  # Suppression du champ status du formulaire

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        current_user = self.request.user

        self.form_validation(form, self.request.user)

        '''
        if current_user.is_superuser or current_user.isSecretary:
            form.instance.status = 'validated'
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
                form.add_error(None, 'Une réservation existante avec un statut autre que "pending" occupe déjà cette '
                                     'salle pendant cette période.')
        '''


        if form.errors:
            return self.form_invalid(form)

        form.instance.save()
        add_to_ics()
        return super().form_valid(form)


def default_room_image(request):
    """
    Renvoie l'image par défaut.
    """
    default_image_path = os.path.join(settings.MEDIA_ROOM_IMAGE)  # Chemin absolu vers l'image par défaut

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
    template_name = 'applicationlists/roomreservation_list.html'
    login_url = 'login'
