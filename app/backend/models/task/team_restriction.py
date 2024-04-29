from django.db import models
from django.utils.translation import gettext_lazy as _

class TeamRestriction(models.TextChoices):
    SOUND = "TT", _("Tontechnik")
    LIGHT = "LT", _("Lichttechnik")
    OFFICE = "VW", _("Verwaltung")
    NONE = "NO", _("Ohne")
