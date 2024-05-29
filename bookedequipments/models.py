from datetime import date, datetime, time
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from equipments.models import EquipmentCategory


class BookedEquipment(models.Model):
    STATUS_CHOICES = [
        ('loaned', 'prêté'),
        ('canceled', 'annulé'),
        ('back', 'rendu'),
        ('late', 'en retard')
    ]

    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    groups = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    motif = models.CharField(max_length=100)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    equipment_category = models.ForeignKey(
        EquipmentCategory,
        on_delete=models.CASCADE,
    )

    def perform_validations(self):
        # Vérifiez que l'utilisateur existe avant de vérifier is_superuser
        if self.user and (self.user.is_superuser or self.user.isSecretary):
            return  # Ignorer toutes les validations si l'utilisateur est un superutilisateur

        # Vérification de la validité de la date et de l'heure de début
        selected_date = self.date
        if selected_date < date.today():  # Si la date est antérieure à aujourd'hui
            raise ValidationError('Vous ne pouvez pas choisir une date antérieure à aujourd\'hui.')

        start_time = self.startTime
        if start_time:
            # Vérification de l'heure de début dans les plages horaires autorisées
            if start_time < time(8, 0) or start_time > time(18, 0):
                raise ValidationError('L\'heure de début doit être entre 8h00 et 18h00.')

            # Vérification de l'heure de début pour la même journée
            if selected_date == date.today():
                current_time = datetime.now().time()
                new_hour = current_time.hour + 1
                new_minute = current_time.minute + 30
                if new_minute >= 60:
                    new_hour += 1
                    new_minute -= 60
                min_start_time = time(new_hour, new_minute)
                if start_time <= min_start_time:
                    raise ValidationError('L\'heure de début doit être supérieure à 1h30 de l\'heure actuelle.')

        end_time = self.endTime
        if end_time:
            # Vérification de l'heure de fin dans les plages horaires autorisées
            if end_time < time(8, 0) or end_time > time(18, 0):
                raise ValidationError('L\'heure de fin doit être entre 8h00 et 18h00.')
            if end_time <= start_time:
                raise ValidationError('L\'heure de fin doit être supérieure à l\'heure de début.')

        # Ajout de la condition pour le samedi après 12h30 et le dimanche
        if selected_date.weekday() == 5:  # Samedi (0 = lundi, 6 = dimanche)
            if start_time >= time(12, 30):
                raise ValidationError('Aucune réservation possible le samedi après 12h30.')
        elif selected_date.weekday() == 6:  # Dimanche
            raise ValidationError('Aucune réservation possible le dimanche.')

        # Vérification qu'aucune réservation n'occupe la même salle pendant la même période
        existing_bookings = BookedEquipment.objects.filter(
            equipment_category=self.equipment_category,
            date=self.date,
            startTime__lt=self.endTime,
            endTime__gt=self.startTime,
        ).exclude(pk=self.pk)

        # Filtrer les réservations existantes avec un statut autre que "pending"
        existing_non_pending_bookings = existing_bookings.exclude(status='pending')

        if existing_non_pending_bookings.exists():
            raise ValidationError(
                'Une réservation existante avec un statut autre que "pending" occupe déjà cet équipement pendant cette '
                'période.')

    def get_absolute_url(self):
        return reverse('bookedequipments_detail', args=[str(self.id)])

    def __str__(self):
        return self.equipment_category.libRoom + " |  " + self.user.username
