from django.db import models
from .user import User

class Adress(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    street = models.CharField("Straße", blank=True, max_length=40)
    house_number = models.CharField("Hausnummer", blank=True, max_length=40)
    postal_code = models.CharField("PLZ", blank=True, max_length=40)
    country = models.CharField("Land", blank=True, max_length=40) #maybe as an option field

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adressen"

    def __str__(self):
        return str(self.username) + "\'s Adresse"
