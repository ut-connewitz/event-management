from django.db import models
from django.utils.timezone import now
from django.db.utils import IntegrityError
from .event import Event


class EventDay(models.Model):
    event_day_id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField("Datum", null=True, blank=True)
    #making start time unique assuming there can not be two events beginning at the exact same time within the ut
    #standard exception handling seems viable
    #NOTE: making this field pk will add duplicate instance with newly set time on update
    start_time = models.DateTimeField("Veranstaltungsbeginn", default=now, unique=True)
    duration = models.DurationField("Veranstaltungsdauer", null=True, blank=True) #TODO: test how this works
    admission_time = models.DateTimeField("Einlassbeginn", null=True, blank=True)

    class Meta:
        verbose_name = "Veranstaltungstag"
        verbose_name_plural = "Veranstaltungstage"

    def __str__(self):
        return str(self.event) + " " + str(self.date)

    # overwrite save methods with caution!
    # this is meant to prevent db crash wenn multiple event days with equal starting times are entered from addtestdata.py
    # this may occur, when addtestdata.py is run multiple times for development/testing reasons
    # for now, only unique fields are problematic since primary key duplicates just wont be inserted (as expected) without crashing the db
    # exception handling in the admin panel is not affected
    def save(self, *args, **kwargs):
        try:
            super(EventDay, self).save(*args, **kwargs)
        except IntegrityError:
            print("Zu dieser Zeit findet bereits eine Veranstaltung statt")
            pass