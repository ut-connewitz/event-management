from django.db import models
from django.utils.translation import gettext_lazy as _

class ConfirmationType(models.TextChoices):
    NOT = "NO", _("Nicht")
    CERTAIN = "CE", _("Sicher")
    MAYBE = "MB", _("Vielleicht")
