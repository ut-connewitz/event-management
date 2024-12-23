from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.db.utils import IntegrityError
from .event_series import EventSeries
from .location import Location

from datetime import datetime


class PastEvent(models.Model):
    past_event_id = models.BigAutoField(primary_key=True)
    series = models.ForeignKey(
        EventSeries,
        on_delete=models.CASCADE,
        verbose_name = "Veranstaltungsreihe",
    )
    subtitle = models.TextField(
        "Veranstaltungsname",
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
    )
    duration = models.PositiveIntegerField(
        "Veranstaltungsdauer",
        null=True,
        blank=True,
        help_text="(Dauer in Minuten)"
    )
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
        verbose_name = "Vergangene Veranstaltung"
        verbose_name_plural = "Vergangene Veranstaltungen"

        ordering = ["date"]

    def __str__(self):
        return str(self.series) + " " + str(self.date.strftime('%d.%m.%Y'))

    # overwrite save methods with caution!
    # this is meant to prevent db crash wenn multiple event days with equal starting times are entered from addtestdata.py
    # this may occur, when addtestdata.py is run multiple times for development/testing reasons
    # for now, only unique fields are problematic since primary key duplicates just wont be inserted (as expected) without crashing the db
    # exception handling in the admin panel is not affected
    def save(self, *args, **kwargs):
        try:
            super(PastEvent, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass

    @property
    def get_html_url(self):
        url = reverse('events_calendar:past_event_edit', args=(self.past_event_id,))
        return f'<a href="{url}"> {self.series.event_name} </a>'
