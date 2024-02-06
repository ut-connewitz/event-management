from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

class EventType(models.TextChoices):
    CINEMA = "CI", _("Kino")
    CONCERT = "CO", _("Musik")
    PLAY = "PL", _("Bühne")
    PARTY = "PY", _("Party")
    EXTRA = "EX", _("Extra")
    FESTIVAL = "FV", _("Festival")
    OTHER = "OT", _("Sonstiges")

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

class EventDay(models.Model):
    event_day_id = models.BigAutoField(primary_key=True)
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE)
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
        return str(self.event_name) + str(self.date)

class Act(models.Model):
    act_name = models.CharField(
        "Aktname",
        max_length=40,
        primary_key=True
    )
    person_count = models.PositiveIntegerField("Personenzahl", null=True, blank=True)
    act_image = models.ImageField("Bild", null=True, blank=True)
    #TODO: test options for music files
    music_sample = models.FileField("Musikbeispiel", null=True, blank=True)
    diet = models.CharField("Ernährung", blank=True, max_length=100)
    act_email = models.EmailField("Email", null=True, blank=True, max_length=100)
    act_phone = models.CharField("Telefon", blank=True, max_length=15)

    class Meta:
        verbose_name = "Akt"
        verbose_name_plural = "Akte"

    def __str__(self):
        return str(self.act_name)

class EventAct(models.Model):
    event_act_id = models.BigAutoField(primary_key=True)
    event_day = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    act_name = models.ForeignKey(Act, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Auftritt"
        verbose_name_plural = "Auftritte"

    def __str__(self):
        return str(self.event_name) + str(self.act_name)
