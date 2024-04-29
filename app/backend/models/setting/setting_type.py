from django.db import models
from django.utils.translation import gettext_lazy as _

class SettingType(models.TextChoices):
    NOTIFICATION_GLOBAL = "NG", _("Benachrichtigungen allgmein")
    NOTIFICATION_SPECIFIC = "NS", _("Bestimmte Benachrichtigung") #not yet implemented, low prio
    APPEARANCE = "AP", _("Erscheinungsbild")
    MISC_SETTING = "ST", _("Einstellung")
