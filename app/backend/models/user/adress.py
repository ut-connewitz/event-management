from django.db import models
from django.urls import reverse
from .user import User

class Adress(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    street = models.CharField(
        "Straße",
        blank=True,
        max_length=40,
    )
    house_number = models.CharField(
        "Hausnummer",
        blank=True,
        max_length=40,
    )
    postal_code = models.CharField(
        "PLZ",
        blank=True,
        max_length=40,
    )
    country = models.CharField(
        "Land",
        blank=True,
        max_length=40,
    ) #maybe as an option field

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adressen"

    def __str__(self):
        return str(self.user) + "\'s Adresse"

    def get_absolute_url(self):
        return reverse("profile:adress_edit", kwargs={"pk": self.user.pk})
