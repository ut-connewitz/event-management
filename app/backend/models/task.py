from django.db import models
from django.utils.translation import gettext_lazy as _
from .event import EventDay
from .user import User

class Task(models.Model):
    class TaskType(models.TextChoices):
        ADMISSION = "AD", _("Einlass")
        SOUND = "TT", _("Tontechnik")
        LIGHT = "LT", _("Lichttechnik")
        KITCHEN = "KÜ", _("Küche")
        OTHER = "OT", _("Sonstiges")

    class TeamRestriction(models.TextChoices):
        SOUND = "TT", _("Tontechnik")
        LIGHT = "LT", _("Lichttechnik")
        OFFICE = "VW", _("Verwaltung")
        NONE = "NO", _("Ohne")

    class Urgency(models.TextChoices):
        URGENT = "UR", _("Dringend")
        IMPORTANT = "IM", _("Wichtig")
        MEDIUM = "MD", _("Mittel")
        LOW = "LO", _("Niedrig")

    class State(models.TextChoices):
        FREE = "FR", _("Offen")
        TAKEN = "TK", _("Übernommen")
        MAYBE = "MB", _("Vielleicht")
        DONE = "DN", _("Erledigt")

    task_id = models.BigAutoField(primary_key=True)
    event_day_id = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    task_type = models.CharField(
        max_length=2,
        choices=TaskType.choices,
        default=TaskType.OTHER,
    )
    team_restriction = models.CharField(
        max_length=2,
        choices=TeamRestriction.choices,
        default=TeamRestriction.NONE,
    )
    urgency = models.CharField(
        max_length=2,
        choices=Urgency.choices,
        default=Urgency.MEDIUM,
    )
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.FREE,
    )
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    comment = models.TextField()

    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"

    def __str__(self):
        return self.task_id

class Volunteering(models.Model):
    class ConfirmationType(models.TextChoices):
        NOT = "NO", _("Nicht")
        CERTAIN = "CE", _("Sicher")
        MAYBE = "MB", _("Vielleicht")

    volunteering_id = models.BigAutoField(primary_key=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_type = models.CharField(
        max_length=15,
        choices=ConfirmationType.choices,
        default=ConfirmationType.NOT,
    )

    class Meta:
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"

    def __str__(self):
        return self.volunteering_id
