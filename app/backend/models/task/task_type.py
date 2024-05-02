from django.db import models
from django.utils.translation import gettext_lazy as _

class TaskType(models.TextChoices):
    ADMISSION = "AD", _("Einlass")
    SOUND = "TT", _("Tontechnik")
    LIGHT = "LT", _("Lichttechnik")
    KITCHEN = "KÜ", _("Küche")
    BAR = "BR", _("Bar")
    OTHER = "OT", _("Sonstiges")
