from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    isSecretary = models.BooleanField(default=False)