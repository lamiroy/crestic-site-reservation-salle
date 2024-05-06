import os

from django.http import HttpResponse


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
