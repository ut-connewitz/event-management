from django.db import models
from django.db.utils import IntegrityError
from backend.models.misc import Adress

class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    location_name = models.CharField(
        "Name",
        max_length=40,
    )
    adress = models.ForeignKey(
        Adress,
        on_delete=models.CASCADE,
        verbose_name = "Adresse",
    )

    class Meta:
        verbose_name = "Veranstaltungsort"
        verbose_name_plural = "Veranstaltungsorte"
        constraints = [
            models.UniqueConstraint(fields=["location_name"], name="prevent Location name duplicates constraint")
        ]

    def __str__(self):
        return str(self.location_name)

    def save(self, *args, **kwargs):
        try:
            super(Location, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass
