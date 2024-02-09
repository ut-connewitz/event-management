from django.db import models
from django.utils.translation import gettext_lazy as _

class NotificationType(models.TextChoices):
    TASK_NOTIFICATION = "AB", _("Aufgabenbenachrichtigung")
    VOLUNTEERING_NOTIFICATION = "DB", _("Dienstbenachrichtigung")
    MISC_NOTIFICATION = "BN", _("Benachrichtigung")
