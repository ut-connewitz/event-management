from django.db import models
from django.utils.translation import gettext_lazy as _

class ConfirmationType(models.TextChoices):
    NO = "NO", _("Nein")
    YES = "YS", _("Ja")
    #MAYBE = "MB", _("Vielleicht")
