from django.db import models
from django.utils.translation import gettext_lazy as _
from .task import Task, Volunteering


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        TASK_NOTIFICATION = "AB", _("Aufgabenbenachrichtigung")
        VOLUNTEERING_NOTIFICATION = "DB", _("Dienstbenachrichtigung")
        MISC_NOTIFICATION = "BN", _("Benachrichtigung")

    notification_id = models.BigAutoField(primary_key=True)
    notification_type = models.CharField(
        "Benachrichtigungsart",
        max_length=2,
        choices=NotificationType.choices,
        default=NotificationType.MISC_NOTIFICATION,
    )
    comment = models.TextField("Kommentar", blank=True)
    timer = models.PositiveIntegerField("Timer") #alternative: TimeField

    class Meta:
        verbose_name = "Benachrichtigung"
        verbose_name_plural = "Benachrichtigungen"

    def __str__(self):
        return self.notification_id

class TaskNotification(Notification):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Aufgabenbenachrichtigung"
        verbose_name_plural = "Aufgabenbenachrichtigungen"

class VolunteeringNotification(Notification):
    volunteering_id = models.ForeignKey(Volunteering, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Dienstbenachrichtigung"
        verbose_name_plural ="Dienstbenachrichtigungen"
