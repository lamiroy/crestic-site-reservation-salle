from django.db import models
from django.db.models import Sum
from django.urls import reverse


class RoomCategory(models.Model):
    libRoom = models.CharField(max_length=50)
    description = models.TextField(default="Entrez la description")
    image = models.ImageField(upload_to='/upload/', default='/upload/default.jpg')
    maxCapacity = models.IntegerField(default='1')


    def __str__(self):
        return self.libRoom

    def get_absolute_url(self):
        return reverse('roomdashboard_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Room Category'
        verbose_name_plural = 'Room Categories'
