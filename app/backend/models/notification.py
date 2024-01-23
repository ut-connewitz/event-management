from django.db import models

class NotificationType(models.TextChoices):
    TASK_NOTIFICATION = "TN", _("Aufgabenbenachrichtigung")
    VOLUNTEERING_NOTIFICATION = "VN", _("Dienstbenachrichtigung")
    MISC_NOTIFICATION = "MN", _("Benachrichtigung")


class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key=true)
    notification_type = models.CharField(
        max_length=2,
        choices=NotificationType.choices
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
