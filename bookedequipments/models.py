from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from equipments.models import EquipmentCategory


class BookedEquipment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'en attente'),
        ('loaned', 'prêté'),
        ('canceled', 'annulé'),
        ('back', 'rendu'),
        ('late', 'en retard')
    ]

    LABORATORY_CHOICES = [  # Choix pour les groupes de laboratoire
        (None, 'Sélectionnez un laboratoire'),
        ('CReSTIC', 'CReSTIC'),
        ('Lab-i*', 'Lab-i*'),
        ('LICIIS', 'LICIIS'),
        ('Autre', "Autre"),
    ]

    date = models.DateField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    groups = models.CharField(max_length=100, choices=LABORATORY_CHOICES)
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
    last_person_modified = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='modifications_equipement',
        verbose_name='Dernière personne ayant modifié'
    )
    last_date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Dernière date de modification'
    )

    def get_absolute_url(self):
        return reverse('bookedequipments_detail', args=[str(self.id)])

    def __str__(self):
        return self.equipment_category.libEquipment + " |  " + self.user.username
