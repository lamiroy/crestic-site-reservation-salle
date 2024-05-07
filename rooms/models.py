from django.db import models  # Importe les classes de modèle de Django
from django.db.models import Sum  # Importe la fonction Sum de django.db.models pour effectuer des agrégations
from django.urls import reverse  # Importe la fonction reverse pour la résolution d'URLs


class RoomCategory(models.Model):  # Définit une classe de modèle RoomCategory qui hérite de models.Model
    libRoom = models.CharField(max_length=50)  # Champ pour stocker le nom de la salle
    description = models.TextField(
        default="Entrez la description")  # Champ pour stocker la description de la salle avec une valeur par défaut
    image = models.ImageField(upload_to='default_image',
                              default='default_image/default.jpg')  # Champ pour télécharger une image de la salle, avec un répertoire de stockage et une image par défaut spécifiés
    maxCapacity = models.IntegerField(
        default='1')  # Champ pour spécifier la capacité maximale de la salle, avec une valeur par défaut

    def __str__(self):  # Méthode spéciale qui renvoie une représentation en chaîne de caractères de l'objet
        return self.libRoom  # Renvoie le nom de la salle comme représentation en chaîne de caractères

    def get_absolute_url(self):  # Méthode pour obtenir l'URL absolue de l'objet
        return reverse('roomdashboard_detail', args=[str(self.id)])  # Renvoie l'URL de détail de la catégorie de salle

    class Meta:  # Classe imbriquée Meta pour la configuration du modèle
        verbose_name = 'Room Category'  # Nom verbeux pour la classe de modèle (singulier)
        verbose_name_plural = 'Room Categories'  # Nom verbeux pour la classe de modèle (pluriel)
