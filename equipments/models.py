from django.db import models
from django.urls import reverse


class EquipmentCategory(models.Model):
    libEquipment = models.CharField(max_length=50)  # Champ pour stocker le nom de l'équipement

    description = models.TextField(
        default="Entrez la description")  # Champ pour stocker la description de l'équipement avec une valeur par défaut

    image = models.ImageField(upload_to='default_image',
                              default='default_image/default.jpg')  # Champ pour télécharger une image de l'équipement

    nbrEquipments = models.IntegerField(default='1')  # Champ pour spécifier le nombre d'équipements

    def __str__(self):
        return self.libEquipment

    def get_absolute_url(self):
        return reverse('equipmentdashboard_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Equipment Category'
        verbose_name_plural = 'Equipment Categories'
