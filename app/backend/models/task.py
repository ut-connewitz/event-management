from django.db import models

class TaskType(models.TextChoices):
    ADMISSION = "AD", _("Einlass")
    SOUND = "SO", _("Tontechnik")
    LIGHT = "LI", _("Lichttechnik")
    KITCHEN = "KI", _("Küche")
    OTHER = "O", _("Sonstiges")

class TeamRestriction(models.TextChoices):
    SOUND = "SO", _("Tontechnik")
    LIGHT = "LI", _("Lichttechnik")
    OFFICE = "OF", _("Verwaltung")
    NONE = "NO", _("Ohne")

class Urgency(models.TextChoices):
    URGENT = "HI", _("Dringend")
    IMPORTANT = "IM", _("Wichtig")
    MEDIUM = "ME", _("Mittel")
    LOW = "LO", _("Niedrig")

class State(models.TextChoices):
    FREE = "FR", _("Offen")
    TAKEN = "TA", _("Übernommen")
    MAYBE = "MB", _("Vielleicht")
    DONE = "DN", _("Erledigt")

class ConfirmationType(models.TextChoices):
    NOT = "NO", _("Nicht")
    CERTAIN = "CE", _("Sicher")
    MAYBE = "MB", _("Vielleicht")

class Task(models.Model):
    task_id = models.BigAutoField(primary_key=true)
    task_type = models.CharField(
        max_length=2,
        choices=TaskType.choices
        default=TaskType.OTHER)
    team_restriction = models.CharField(
        max_length=2,
        choices=TeamRestriction.choices
        default=TeamRestriction.NONE)
    urgency = models.CharField(
        max_length=2,
        choices=Urgency.choices
        default=Urgency.MEDIUM)
    state = models.CharField(
        max_length=2,
        choices=State.choices
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
    volunteering_id = models.BigAutoField(primary_key=true)
    task_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_type = models.CharField(
        max_length=2,
        choices=ConfirmationType.choices
        default=ConfirmationType.NOT)

    class Meta:
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"

    def __str__(self):
        return self.volunteering_id
