from django.db import models
from django.utils.translation import gettext_lazy as _

class Urgency(models.TextChoices):
    URGENT = "UR", _("Dringend")
    IMPORTANT = "IM", _("Wichtig")
    MEDIUM = "MD", _("Mittel")
    LOW = "LO", _("Niedrig")
