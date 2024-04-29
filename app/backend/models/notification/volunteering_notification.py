from django.db import models
from backend.models.task.volunteering import Volunteering
from backend.models.notification.notification import Notification

class VolunteeringNotification(Notification):
    volunteering = models.ForeignKey(Volunteering, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Dienstbenachrichtigung"
        verbose_name_plural ="Dienstbenachrichtigungen"
