from django.db import models
from .event_type import EventType

class EventSeries(models.Model):
    series_id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(
        "Name der Vorlage",
        help_text="Der Name der Vorlage erscheint als Name der daraus erstellten Veranstaltungen und kann dabei optional um einen Veranstaltungstitel erweitert werden.",
        max_length=50,
    )
    event_type = models.CharField(
        "Veranstaltungsart",
        max_length=2,
        choices=EventType.choices,
        default=EventType.OTHER,
    )
    event_description = models.TextField(
        "Beschreibung",
        blank=True,
        max_length=800
    )
    event_press = models.TextField(
        "Pressetext",
        blank=True,
        max_length=800
        )
    event_fee = models.DecimalField(
        "Einlassgebühr",
        null=True,
        blank=True,
        max_digits=4,
        decimal_places=2,
    )
    event_image = models.ImageField(
        "Bild",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Veranstaltungsvorlage"
        verbose_name_plural = "Veranstaltungsvorlagen"

    def __str__(self):
        return str(self.event_name)
