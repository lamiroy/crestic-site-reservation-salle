from django.db import models
from django.urls import reverse

from RoomQueSTIC.settings import MEDIA_EQUIPMENT_IMAGE


class EquipmentCategory(models.Model):
    libEquipment = models.CharField(max_length=50)  # Champ pour stocker le nom de l'équipement

    description = models.TextField(
        default="Entrez la description")  # Champ pour stocker la description de l'équipement avec une valeur par défaut

    image = models.ImageField(upload_to='default-equipment_image',
                              default=MEDIA_EQUIPMENT_IMAGE)  # Champ pour télécharger une image de l'équipement

    def __str__(self):
        return self.libEquipment

    def get_absolute_url(self):
        return reverse('equipmentdashboard_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Equipment Category'
        verbose_name_plural = 'Equipment Categories'
