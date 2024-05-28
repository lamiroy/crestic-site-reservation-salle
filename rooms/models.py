from django.db import models  # Importe les classes de modèle de Django
from django.urls import reverse  # Importe la fonction reverse pour la résolution d'URLs
from RoomQueSTIC.settings import MEDIA_ROOM_IMAGE


class RoomCategory(models.Model):  # Définit une classe de modèle RoomCategory qui hérite de models.Model
    libRoom = models.CharField(max_length=50)  # Champ pour stocker le nom de la salle

    description = models.TextField(
        default="Entrez la description")  # Champ pour stocker la description de la salle avec une valeur par défaut

    image = models.ImageField(upload_to='default_room_image',
                              default=MEDIA_ROOM_IMAGE)  # Champ pour télécharger une image de la salle

    maxCapacity = models.IntegerField(default='1')  # Champ pour spécifier la capacité maximale de la salle

    def __str__(self):
        return self.libRoom  # Renvoie le nom de la salle comme représentation en chaîne de caractères

    def get_absolute_url(self):
        return reverse('roomdashboard_detail', args=[str(self.id)])  # Renvoie l'URL de détails de la salle

    class Meta:
        verbose_name = 'Room Category'
        verbose_name_plural = 'Room Categories'
