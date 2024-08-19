from datetime import datetime

from django.db import models
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils.timezone import now

from .event_series import EventSeries
from .location import Location

class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    series = models.ForeignKey(
        EventSeries,
        on_delete=models.CASCADE,
        verbose_name = "Veranstaltungsvorlage",
    )
    subtitle = models.TextField(
        "Veranstaltungstitel",
        max_length=100,
        blank=True,
    )
    date = models.DateField(
        "Datum",
        null=False,
        blank=False,
    )
    start_time = models.TimeField(
        "Veranstaltungsbeginn",
        default=now,
    )
    admission_time = models.TimeField(
        "Einlassbeginn",
        null=True,
        blank=True,
    )
    duration = models.PositiveIntegerField(
        "Veranstaltungsdauer",
        null=True,
        blank=True,
        help_text="(in Minuten: '127' für 2 h 7 min)"
    ) #TODO: test how this works
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Ort",
    )
    comment = models.TextField(
        "Kommentar",
        max_length=800,
        blank=True,
    )

    class Meta:
        verbose_name = "Veranstaltung"
        verbose_name_plural = "Veranstaltungen"

        constraints = [
            models.UniqueConstraint(fields=["date", "start_time", "location"], name="prevent event duplicates constraint")
        ]

        ordering = ["date"]

    def __str__(self):
        if self.subtitle is not None:
            return str(self.series) + " " + str(self.subtitle) + " " + str(self.date.strftime('%d.%m.%Y'))
        return str(self.series) + " " + str(self.date.strftime('%d.%m.%Y'))

    # overwrite save methods with caution!
    # this is meant to prevent db crash wenn multiple event days with equal starting times are entered from addtestdata.py
    # this may occur, when addtestdata.py is run multiple times for development/testing reasons
    # for now, only unique fields are problematic since primary key duplicates just wont be inserted (as expected) without crashing the db
    # exception handling in the admin panel is not affected
    def save(self, *args, **kwargs):
        try:
            super(Event, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass

    @property
    def get_html_url(self):
        url = reverse('events_calendar:event_edit', args=(self.event_id,))
        return f'<a href="{url}">{self.series.event_name} {self.subtitle}</a>'
