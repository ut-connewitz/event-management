from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.db.utils import IntegrityError
from .event_series import EventSeries


class Event(models.Model):
    event_id = models.BigAutoField(primary_key=True)
    series = models.ForeignKey(
        EventSeries,
        on_delete=models.CASCADE,
        verbose_name = "Veranstaltungsreihe",
    )
    date = models.DateField(
        "Datum",
        null=False,
        blank=False,
        default=now,
    )
    start_time = models.TimeField(
        "Veranstaltungsbeginn",
        default=now,
    )
    duration = models.DurationField(
        "Veranstaltungsdauer",
        null=True,
        blank=True,
    ) #TODO: test how this works
    admission_time = models.TimeField(
        "Einlassbeginn",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Veranstaltung"
        verbose_name_plural = "Veranstaltungen"

        constraints = [
        models.UniqueConstraint(fields=["date", "start_time"], name="prevent event duplicates constraint")
        ]

    def __str__(self):
        return str(self.series) + " " + str(self.date)

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
        return f'<a href="{url}"> {self.series.event_name} </a>'
