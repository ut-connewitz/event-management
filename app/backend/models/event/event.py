from django.db import models
from .event_type import EventType

class Event(models.Model):
    event_name = models.CharField(
        "Veranstaltungsname",
        max_length=50,
        primary_key=True,
    )
    event_type = models.CharField(
        "Veranstaltungsart",
        max_length=2,
        choices=EventType.choices,
        default=EventType.OTHER,
    )
    event_description = models.TextField("Beschreibung", blank=True)
    event_press = models.TextField("Pressetext", blank=True)
    event_fee = models.DecimalField(
        "Einlassgebühr",
        null=True,
        blank=True,
        max_digits=4,
        decimal_places=2,
    )
    event_image = models.ImageField("Bild", null=True, blank=True)

    class Meta:
        verbose_name = "Veranstaltung"
        verbose_name_plural = "Veranstaltungen"

    def __str__(self):
        return str(self.event_name)
