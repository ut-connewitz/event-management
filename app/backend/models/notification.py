from django.db import models
from .task import Task, Volunteering

class NotificationType(models.TextChoices):
    TASK_NOTIFICATION = "Aufgabenbenachrichtigung"
    VOLUNTEERING_NOTIFICATION = "Dienstbenachrichtigung"
    MISC_NOTIFICATION = "Benachrichtigung"


class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        default=NotificationType.MISC_NOTIFICATION)
    comment = models.TextField()
    timer = models.PositiveIntegerField() #alternative: TimeField

    class Meta:
        verbose_name = "Benachrichtigung"
        verbose_name_plural = "Benachrichtigungen"

    def __str__(self):
        return self.notification_id

class TaskNotification(Notification):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

class VolunteeringNotification(Notification):
    volunteering_id = models.ForeignKey(Volunteering, on_delete=models.CASCADE)
