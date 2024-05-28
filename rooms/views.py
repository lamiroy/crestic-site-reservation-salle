from django.http import HttpResponse  # Importe la classe HttpResponse pour gérer les réponses HTTP
from django.views.generic import ListView  # Importe la classe ListView pour afficher une liste d'objets
from django.urls import reverse_lazy  # Importe la fonction reverse_lazy pour les URL asynchrones
from RoomQueSTIC import settings  # Importe les paramètres du projet
from .models import RoomCategory  # Importe le modèle RoomCategory
from bookedrooms.models import BookedRoom  # Importe le modèle BookedRoom
from bootstrap_datepicker_plus import (
    DatePickerInput,  # Import du widget DatePickerInput de Bootstrap
    TimePickerInput,  # Import du widget TimePickerInput de Bootstrap
)
from django.contrib.auth.mixins import \
    LoginRequiredMixin  # Importe le mixin LoginRequiredMixin pour les vues basées sur les classes
from django.views.generic.edit import CreateView  # Import de la classe CreateView pour créer des objets dans une vue
from icalendar import (
    Calendar,  # Import du module Calendar de la bibliothèque iCalendar
    Event,  # Import du module Event de la bibliothèque iCalendar
)
from datetime import datetime  # Import de la classe datetime pour manipuler les dates et heures
import os  # Importe le module os pour les opérations sur le système d'exploitation
import json  # Import du module json pour la manipulation de données JSON


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


class HomePageView(LoginRequiredMixin, CreateView):
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
        """
        Surcharge pour toujours définir l'utilisateur sur l'utilisateur actuellement connecté.
        """

