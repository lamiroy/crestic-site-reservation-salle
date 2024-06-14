import os  # Import du module os pour interagir avec le système d'exploitation
import pandas as pd  # Import de la bibliothèque pandas pour la manipulation de données
from django.http import HttpResponse  # Import de la classe HttpResponse pour créer des réponses HTTP
from django.contrib.auth.decorators import user_passes_test  # Import du décorateur pour restreindre l'accès aux users
from bookedrooms.models import BookedRoom  # Import du modèle BookedRoom pour les réservations de salles
from bookedequipments.models import BookedEquipment
from django.utils.timezone import is_aware, make_naive
import datetime


def admin_required(user):
    # Vérifie si l'utilisateur est un administrateur
    return user.is_superuser or user.isSecretary


def export_holiday_ics(request):
    # Chemin absolu vers le fichier .ics existant
    current_directory = os.path.dirname(__file__)
    ics_file_path = os.path.join(current_directory, 'calendarFiles/calendarHoliday.ics')

    # Vérifie si le fichier existe
    if os.path.exists(ics_file_path):
        # Lit le contenu du fichier .ics
        with open(ics_file_path, 'rb') as f:
            ics_content = f.read()

        # Renvoie le contenu .ics en réponse à la requête
        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="calendarHoliday.ics"'

        return response
    else:
        # Génère une réponse 404 si le fichier n'existe pas
        return HttpResponse('Fichier .ics non trouvé', status=404)


def export_bookedrooms_ics(request):
    # Chemin absolu vers le fichier .ics existant
    current_directory = os.path.dirname(__file__)
    ics_file_path = os.path.join(current_directory, 'calendarFiles/calendarBookedroom.ics')

    # Vérifie si le fichier existe
    if os.path.exists(ics_file_path):
        # Lit le contenu du fichier .ics
        with open(ics_file_path, 'rb') as f:
            ics_content = f.read()

        # Renvoie le contenu .ics en réponse à la requête
        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="calendarBookedroom.ics"'

        return response
    else:
        # Génère une réponse 404 si le fichier n'existe pas
        return HttpResponse('Fichier .ics non trouvé', status=404)


def export_bookedroomsNOJSON_ics(request):
    # Chemin absolu vers le fichier .ics existant
    current_directory = os.path.dirname(__file__)
    ics_file_path = os.path.join(current_directory, 'calendarFiles/calendrier_reservation.ics')

    # Vérifie si le fichier existe
    if os.path.exists(ics_file_path):
        # Lit le contenu du fichier .ics
        with open(ics_file_path, 'rb') as f:
            ics_content = f.read()

        # Renvoie le contenu .ics en réponse à la requête
        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="calendrier_reservation.ics"'

        return response
    else:
        # Génère une réponse 404 si le fichier n'existe pas
        return HttpResponse('Fichier .ics non trouvé', status=404)


def export_bookedequipments_ics(request):
    # Chemin absolu vers le fichier .ics existant
    current_directory = os.path.dirname(__file__)
    ics_file_path = os.path.join(current_directory, 'calendarFiles/calendarBookedequipments.ics')

    # Vérifie si le fichier existe
    if os.path.exists(ics_file_path):
        # Lit le contenu du fichier .ics
        with open(ics_file_path, 'rb') as f:
            ics_content = f.read()

        # Renvoie le contenu .ics en réponse à la requête
        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="calendarBookedequipments.ics"'

        return response
    else:
        # Génère une réponse 404 si le fichier n'existe pas
        return HttpResponse('Fichier .ics non trouvé', status=404)

def export_bookedequipmentsNOJSON_ics(request):
    # Chemin absolu vers le fichier .ics existant
    current_directory = os.path.dirname(__file__)
    ics_file_path = os.path.join(current_directory, 'calendarFiles/calendrier_reservation_equipement.ics')

    # Vérifie si le fichier existe
    if os.path.exists(ics_file_path):
        # Lit le contenu du fichier .ics
        with open(ics_file_path, 'rb') as f:
            ics_content = f.read()

        # Renvoie le contenu .ics en réponse à la requête
        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="calendrier_reservation_equipement.ics"'

        return response
    else:
        # Génère une réponse 404 si le fichier n'existe pas
        return HttpResponse('Fichier .ics non trouvé', status=404)


@user_passes_test(admin_required)
def export_to_excel_room(request):
    # Chemin absolu vers le dossier 'excel'
    current_directory = os.path.dirname(__file__)
    excel_directory = os.path.join(current_directory, 'excel')
    if not os.path.exists(excel_directory):
        os.makedirs(excel_directory)

    # Nom du fichier Excel
    excel_file_path = os.path.join(excel_directory, 'reservations_salles.xlsx')

    # Récupérer les données de votre modèle
    data = BookedRoom.objects.select_related('user', 'room_category', 'last_person_modified').all().values(
        'id', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif', 'peopleAmount', 'user__username',
        'room_category__libRoom', 'last_person_modified__username', 'last_date_modified'
    )

    # Convertir les champs datetime en naïfs
    for record in data:
        for field in ['date', 'startTime', 'endTime', 'last_date_modified']:
            if isinstance(record[field], datetime.datetime) and is_aware(record[field]):
                record[field] = make_naive(record[field])

    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(data)

    column_mapping = {
        'id': 'ID',
        'date': 'Date',
        'startTime': 'Début réservation',
        'endTime': 'Fin réservation',
        'groups': 'Laboratoire',
        'status': 'Statut actuel',
        'motif': 'Motif',
        'peopleAmount': 'Nombre de personnes',
        'user__username': 'Demandeur',
        'room_category__libRoom': 'Numéro de la salle',
        'last_person_modified__username': 'Dernière personne ayant modifié',
        'last_date_modified': 'Dernière modification en date',
    }
    df.rename(columns=column_mapping, inplace=True)

    # Écrire les données dans un fichier Excel
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

    # Vérifie si le fichier a été créé
    if os.path.exists(excel_file_path):
        # Lit le contenu du fichier Excel
        with open(excel_file_path, 'rb') as f:
            excel_content = f.read()

        # Renvoie le contenu Excel en réponse à la requête
        response = HttpResponse(excel_content,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="reservations_salles.xlsx"'

        return response
    else:
        # Génère une réponse 404 si le fichier n'existe pas
        return HttpResponse('Fichier Excel non trouvé', status=404)


@user_passes_test(admin_required)
def export_to_excel_equipment(request):
    # Chemin absolu vers le dossier 'excel'
    current_directory = os.path.dirname(__file__)
    excel_directory = os.path.join(current_directory, 'excel')
    if not os.path.exists(excel_directory):
        os.makedirs(excel_directory)

    # Nom du fichier Excel
    excel_file_path = os.path.join(excel_directory, 'reservations_equipements.xlsx')

    # Récupérer les données de votre modèle
    data = BookedEquipment.objects.select_related('user', 'equipment_category', 'last_person_modified').all().values(
        'id', 'date', 'startTime', 'endTime', 'groups', 'status', 'motif', 'user__username',
        'equipment_category__libEquipment', 'last_person_modified__username', 'last_date_modified'
    )

    # Convertir les champs datetime en naïfs
    for record in data:
        for field in ['date', 'startTime', 'endTime', 'last_date_modified']:
            if isinstance(record[field], datetime.datetime) and is_aware(record[field]):
                record[field] = make_naive(record[field])

    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(data)

    column_mapping = {
        'id': 'ID',
        'date': 'Date',
        'startTime': 'Début réservation',
        'endTime': 'Fin réservation',
        'groups': 'Laboratoire',
        'status': 'Statut actuel',
        'motif': 'Motif',
        'user__username': 'Demandeur',
        'equipment_category__libEquipment': 'Nom de l\'équipement',
        'last_person_modified__username': 'Dernière personne ayant modifié',
        'last_date_modified': 'Dernière modification en date',
    }
    df.rename(columns=column_mapping, inplace=True)

    # Écrire les données dans un fichier Excel
    df.to_excel(excel_file_path, index=False, engine='openpyxl')

    # Vérifie si le fichier a été créé
    if os.path.exists(excel_file_path):
        # Lit le contenu du fichier Excel
        with open(excel_file_path, 'rb') as f:
            excel_content = f.read()

        # Renvoie le contenu Excel en réponse à la requête
        response = HttpResponse(excel_content,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="reservations_equipements.xlsx"'

        return response
    else:
        # Génère une réponse 404 si le fichier n'existe pas
        return HttpResponse('Fichier Excel non trouvé', status=404)
