from django.db import models
from django.utils.translation import gettext_lazy as _

class EventType(models.TextChoices):
    CINEMA = "CI", _("Kino")
    CONCERT = "CO", _("Musik")
    PLAY = "PL", _("Bühne")
    PARTY = "PY", _("Party")
    EXTRA = "EX", _("Extra")
    FESTIVAL = "FV", _("Festival")
    OTHER = "OT", _("Sonstiges")
