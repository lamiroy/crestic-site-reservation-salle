from django.contrib.auth import get_user_model  # Import de la fonction pour obtenir le modèle utilisateur personnalisé
from rooms.models import RoomCategory  # Import du modèle RoomCategory pour les catégories de salles
from django.db import models  # Import du module models pour définir les modèles de la base de données
from django.urls import reverse  # Import de la fonction reverse pour obtenir les URL inversées

class BookedRoom(models.Model):
    STATUS_CHOICES = [  # Choix pour le statut de la réservation
        ('pending', 'En attente'),
        ('canceled', 'Annulé'),
        ('validated', 'Validé'),
    ]

    LABORATORY_CHOICES = [  # Choix pour les groupes de laboratoire
        (None, 'Sélectionnez un laboratoire'),
        ('CReSTIC', 'CReSTIC'),
        ('Lab-i*', 'Lab-i*'),
        ('LICIIS', 'LICIIS'),
        ('Autre', "Autre"),
    ]

    date = models.DateField()  # Date de la réservation
    startTime = models.TimeField()  # Heure de début de la réservation
    endTime = models.TimeField()  # Heure de fin de la réservation
    groups = models.CharField(max_length=100, choices=LABORATORY_CHOICES)  # Groupe de laboratoire
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,
                              default=STATUS_CHOICES[0][0])  # Statut de la réservation
    motif = models.CharField(max_length=100)  # Motif de la réservation
    peopleAmount = models.IntegerField(default=1)  # Nombre de personnes
    user = models.ForeignKey(  # Utilisateur associé à la réservation
        get_user_model(),  # Utilisation de la fonction get_user_model pour obtenir le modèle utilisateur personnalisé
        on_delete=models.CASCADE,  # Suppression en cascade de l'utilisateur si celui-ci est supprimé
    )
    room_category = models.ForeignKey(  # Catégorie de salle réservée
        RoomCategory,  # Utilisation du modèle RoomCategory pour les catégories de salles
        on_delete=models.CASCADE,  # Suppression en cascade de la catégorie de salle si celle-ci est supprimée
    )
    last_person_modified = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='modifications',
        verbose_name='Dernière personne ayant modifié'
    )
    last_date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Dernière date de modification'
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            print(f'creating object {self.pk}')
        else:
            print(f'updating object {self.pk}')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Renvoie l'URL absolue de l'objet BookedRoom, utilisée pour les redirections après une création ou une
        # modification
        return reverse('bookedrooms_detail', args=[str(self.id)])

    def __str__(self):
        # Renvoie une représentation en chaîne de caractères de l'objet BookedRoom, utilisée notamment dans
        # l'interface d'administration Django
        return self.room_category.libRoom + " |  " + self.user.username



