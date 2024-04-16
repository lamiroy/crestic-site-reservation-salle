from django.db import models
from django.db.models import Sum
from django.urls import reverse


class RoomCategory(models.Model):
    nom_de_la_salle = models.CharField(max_length=50)
    description = models.TextField()
    nombre_de_personnes = models.IntegerField()
    motif_de_reservation = models.CharField(max_length=150, default='')
    image_de_la_salle = models.ImageField(
        upload_to='images/roomCategories',
        default='images/roomCategories/none.png'
    )


    def __str__(self):
        return self.nom_de_la_salle

    def get_absolute_url(self):
        return reverse('roomdashboard_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Room Category'
        verbose_name_plural = 'Room Categories'
