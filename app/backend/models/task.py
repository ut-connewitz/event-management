from django.db import models
from .event import EventDay
from .user import User

class TaskType(models.TextChoices):
    ADMISSION = "Einlass"
    SOUND = "Tontechnik"
    LIGHT = "Lichttechnik"
    KITCHEN = "Küche"
    OTHER = "Sonstiges"

class TeamRestriction(models.TextChoices):
    SOUND = "Tontechnik"
    LIGHT = "Lichttechnik"
    OFFICE = "Verwaltung"
    NONE = "Ohne"

class Urgency(models.TextChoices):
    URGENT = "Dringend"
    IMPORTANT = "Wichtig"
    MEDIUM = "Mittel"
    LOW = "Niedrig"

class State(models.TextChoices):
    FREE = "Offen"
    TAKEN = "Übernommen"
    MAYBE = "Vielleicht"
    DONE = "Erledigt"

class ConfirmationType(models.TextChoices):
    NOT = "Nicht"
    CERTAIN = "Sicher"
    MAYBE = "Vielleicht"

class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    event_day_id = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    task_type = models.CharField(
        max_length=15,
        choices=TaskType.choices,
        default=TaskType.OTHER)
    team_restriction = models.CharField(
        max_length=15,
        choices=TeamRestriction.choices,
        default=TeamRestriction.NONE)
    urgency = models.CharField(
        max_length=15,
        choices=Urgency.choices,
        default=Urgency.MEDIUM)
    state = models.CharField(
        max_length=15,
        choices=State.choices,
        default=State.FREE)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    comment = models.TextField()

    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"

    def __str__(self):
        return self.task_id

class Volunteering(models.Model):
    volunteering_id = models.BigAutoField(primary_key=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_type = models.CharField(
        max_length=15,
        choices=ConfirmationType.choices,
        default=ConfirmationType.NOT)

    class Meta:
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"

    def __str__(self):
        return self.volunteering_id
