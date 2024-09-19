from bootstrap_datepicker_plus import (
    DatePickerInput,  # Import du widget DatePickerInput pour la sélection de dates dans les formulaires
    TimePickerInput  # Import du widget TimePickerInput pour la sélection d'heures dans les formulaires
)

from datetime import datetime, date, time

from bookedequipments.models import BookedEquipment
from bookedrooms.models import BookedRoom  # Importe le modèle BookedRoom


class BookedEquipmentGenericView:
    fields = ('equipment_category', 'date', 'startTime', 'endTime', 'groups', 'motif')

    def form_template(self, form):
        """
        Overridden to change the DateFields from text boxes to
        DatePicker widgets
        """
        form.fields['equipment_category'].label = 'Nom de l\'équipment'
        form.fields['date'].label = 'Jour de la réservation'
        form.fields['startTime'].label = 'Début de la réservation'
        form.fields['endTime'].label = 'Fin de la réservation'
        form.fields['groups'].label = 'Laboratoire'
        form.fields['motif'].label = 'Motif'
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        return form

    def form_validation(self, form, current_user):
        """
        Overridden to always set the user to the currently logged-in user
        """
        form.instance.status = 'pending'

        selected_date = form.cleaned_data['date']
        start_time = form.cleaned_data['startTime']
        end_time = form.cleaned_data['endTime']

        if selected_date < date.today():
            form.add_error('date', 'Vous ne pouvez pas choisir une date antérieure à aujourd\'hui.')

        existing_bookings = BookedEquipment.objects.filter(
            equipment_category=form.instance.equipment_category,
            date=selected_date,
            startTime__lt=end_time,
            endTime__gt=start_time,
            status='loaned'
        )

        if existing_bookings.exists():
            form.add_error(None, 'Une réservation existante existe pendant cette période.')

        # Vérifier si l'utilisateur est un secrétaire ou un administrateur
        if not current_user.is_superuser and not current_user.isSecretary:

            # Validation personnalisée
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

        elif not existing_bookings.exists():  # l'utilisateur actuel a le rôle de secrétaire ou est administrateur
            form.instance.status = 'loaned'

        return form

class BookedRoomsGenericView:
    fields = ('room_category', 'peopleAmount', 'date', 'startTime', 'endTime', 'groups', 'motif')

    def form_template(self, form):
        form.fields['room_category'].label = 'Nom de la salle'
        form.fields['peopleAmount'].label = 'Nombre de personnes'
        form.fields['peopleAmount'].widget.attrs['min'] = 1
        form.fields['peopleAmount'].widget.attrs['max'] = 30
        form.fields['date'].label = 'Date de réservation'
        form.fields['date'].widget = DatePickerInput(
            options={
                "locale": "fr",
                "format": "DD/MM/YYYY",
            }
        )
        form.fields['startTime'].label = 'Heure de début'
        form.fields['startTime'].widget = TimePickerInput().start_of('duration')
        form.fields['endTime'].label = 'Heure de fin'
        form.fields['endTime'].widget = TimePickerInput().end_of('duration')
        form.fields['groups'].label = 'Laboratoire'
        form.fields['motif'].label = 'Motif'
        return form

    def form_validation(self, form, user):
        form.instance.status = 'pending'

        selected_date = form.cleaned_data['date']
        if selected_date < date.today():
            form.add_error('date', 'Vous ne pouvez pas choisir une date antérieure à aujourd\'hui.')

        start_time = form.cleaned_data['startTime']
        end_time = form.cleaned_data['endTime']

        existing_bookings = BookedRoom.objects.filter(
            room_category=form.instance.room_category,
            date=selected_date,
            startTime__lt=end_time,
            endTime__gt=start_time,
            status='validated'
        )

        if existing_bookings.exists():
            form.add_error(None, 'Une réservation validée existe déjà pour cette '
                                 'salle pendant cette période.')

        # Vérifier si l'utilisateur est un secrétaire ou un administrateur
        if not user.is_superuser and not user.isSecretary:

            if user != form.instance.user:
                form.add_error(None, 'Cette réservation ne vous appartient pas. Veuillez revenir à la page d\'accueil')
            # Validation personnalisée
            start_time = form.cleaned_data['startTime']
            end_time = form.cleaned_data['endTime']

            if start_time < time(7, 0) or start_time > time(20, 0):
                form.add_error('startTime', 'L\'heure de début doit être entre 7h00 et 20h00.')

            if selected_date == date.today():
                current_time = datetime.now().time()
                new_hour = current_time.hour + 1
                new_minute = current_time.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                min_start_time = time(new_hour, new_minute)
                if start_time <= min_start_time:
                    form.add_error('startTime',
                                   'L\'heure de début doit être supérieure à 1h30 de l\'heure actuelle.')

            if end_time < time(7, 0) or end_time > time(20, 0):
                form.add_error('endTime', 'L\'heure de fin doit être entre 7h00 et 20h00.')
            if end_time <= start_time:
                form.add_error('endTime', 'L\'heure de fin doit être supérieure à l\'heure de début.')

            if selected_date.weekday() == 5 and start_time >= time(12, 30):
                form.add_error('startTime', 'Aucune réservation possible le samedi après 12h30.')
            elif selected_date.weekday() == 6:
                form.add_error('date', 'Aucune réservation possible le dimanche.')

            if form.instance.peopleAmount > form.instance.room_category.maxCapacity:
                form.add_error('peopleAmount', 'Le nombre de personnes dépasse la capacité maximale de la salle.')

        elif not existing_bookings.exists():  # l'utilisateur actuel a le rôle de secrétaire ou est administrateur
            form.instance.status = 'validated'

        return form
