from django.db import models
from django.db.models import Sum
from django.urls import reverse


class EquipmentCategory(models.Model):
    libRoom = models.CharField(max_length=50)
    maxCapacity = models.IntegerField()

    def __str__(self):
        return self.libRoom

    def get_absolute_url(self):
        return reverse('equipmentdashboard_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Equipment Category'
        verbose_name_plural = 'Equipment Categories'
