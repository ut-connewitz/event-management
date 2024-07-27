from django.db import models
from django.utils.translation import gettext_lazy as _

class TaskType(models.TextChoices):
    ADMISSION = "AD", _("Einlass")
    BAR = "BR", _("Bar")
    CLEANING = "RG", _("Reinigung")
    KITCHEN = "KÜ", _("Küche")
    LIGHT = "LT", _("Lichttechnik")
    SOUND = "TT", _("Tontechnik")
    OTHER = "OT", _("Sonstiges")
