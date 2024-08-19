from django.db import models

class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    location_name = models.CharField(
        "Name",
        max_length=40,
    )
    street = models.CharField("Straße", blank=True, max_length=40)
    house_number = models.CharField("Hausnummer", blank=True, max_length=40)
    postal_code = models.CharField("PLZ", blank=True, max_length=40)
    country = models.CharField("Land", blank=True, max_length=40)

    class Meta:
        verbose_name = "Ort"
        verbose_name_plural = "Orte"

    def __str__(self):
        return str(self.location_name)
