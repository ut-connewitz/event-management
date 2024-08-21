from django.db import models
from django.db.utils import IntegrityError
from .event_type import EventType

class EventSeries(models.Model):
    series_id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(
        "Name der Reihe",
        help_text="Der Name der Reihe bildet den ersten Teil des Namens der daraus erstellten Veranstaltungen und kann dabei optional um einen Veranstaltungstitel erweitert werden.",
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
        ordering = ["event_name"]
        verbose_name = "Veranstaltungsreihe"
        verbose_name_plural = "Veranstaltungsreihen"
        constraints = [
            models.UniqueConstraint(fields=["event_name"], name="prevent EventSeries name duplicates constraint")
        ]

    def __str__(self):
        return str(self.event_name)

    def save(self, *args, **kwargs):
        try:
            super(EventSeries, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass
