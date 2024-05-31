import os

from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from RoomQueSTIC import settings
from bookedequipments.models import BookedEquipment
from .models import EquipmentCategory

def add_to_ics():
    return None

class EquipmentListView(ListView):
    """
    Affiche une liste des catégories de chambres disponibles.
    """
    model = EquipmentCategory
    template_name = 'equipmentreservation_list.html'
    login_url = 'login'

def default_equipment_image(request):
    """
    Renvoie l'image par défaut.
    """
    default_image_path = os.path.join(settings.MEDIA_EQUIPMENT_IMAGE)  # Chemin absolu vers l'image par défaut

    # Vérifie si l'image par défaut existe
    if os.path.exists(default_image_path):
        with open(default_image_path, 'rb') as f:
            image_content = f.read()  # Lit le contenu de l'image par défaut
        return HttpResponse(image_content, content_type='image/jpeg')  # Renvoie le contenu de l'image en réponse
    else:
        return HttpResponse(status=404)



class HomePageViewEquipment(LoginRequiredMixin, CreateView):
    """
    Affiche la page d'accueil et gère la création de réservations de chambres.
    """
    model = BookedEquipment  # Spécifie le modèle utilisé pour la création d'objets dans la vue
    template_name = 'home_equipment.html'  # Spécifie le modèle de template utilisé pour rendre la vue
    fields = ('equipment_category', 'date', 'startTime', 'endTime', 'groups', 'motif')
    success_url = reverse_lazy('home')  # Spécifie l'URL de redirection après une soumission réussie du formulaire
    login_url = 'login'  # Spécifie l'URL de connexion pour les utilisateurs non authentifiés

    def get_form(self):
        """
        Surcharge pour changer les DateFields en widgets DatePicker.
        """
        form = super(HomePageViewEquipment, self).get_form()
        form.fields['equipment_category'].label = 'Nom de l''équipment'  # Changement de l'étiquette du champ room_category

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
        user = self.request.user

        form.instance.user = user
        try:
            data = super().form_valid(form)
        except ValidationError as e:
            # Convertir l'erreur de validation en chaîne de caractères
            error_message = ', '.join(e.messages)
            # Ajouter l'erreur de validation au formulaire
            form.add_error(None, error_message)

            return self.form_invalid(form)

        # send_reservation_confirmation_email_admin(form.instance)
        add_to_ics()

        return data
