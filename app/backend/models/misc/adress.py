from django.db import models
from django.urls import reverse

class Adress(models.Model):
    adress_id = models.BigAutoField(primary_key=True)
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
        ordering = ["country", "postal_code", "street", "house_number"]
        verbose_name = "Adresse"
        verbose_name_plural = "Adressen"

    def __str__(self):
        adress_string = ''
        if self.street:
            adress_string += str(self.street)
        if self.house_number:
            if adress_string == '':
                adress_string += str(self.house_number)
            else:
                adress_string += ", " + str(self.house_number)
        if self.postal_code:
            if adress_string == '':
                adress_string += str(self.postal_code)
            else:
                adress_string += ", " + str(self.postal_code)
        if self.country:
            if adress_string == '':
                adress_string += str(self.country)
            else:
                adress_string += ", " + str(self.country)
        return  adress_string

    def get_absolute_url(self):
        return reverse("profile:adress_edit", kwargs={"pk": self.pk})
