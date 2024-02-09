from django.db import models
from .notification_type import NotificationType

class Notification(models.Model):
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
        return str(self.notification_id)
