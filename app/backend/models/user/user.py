from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField("Telefon", blank=True, max_length=20)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        app_label = "backend"

    def __str__(self):
        return str(self.username)
