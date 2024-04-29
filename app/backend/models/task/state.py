from django.db import models
from django.utils.translation import gettext_lazy as _

class State(models.TextChoices):
    FREE = "FR", _("Offen")
    TAKEN = "TK", _("Übernommen")
    MAYBE = "MB", _("Vielleicht")
    DONE = "DN", _("Erledigt")
