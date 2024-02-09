from django.db import models
from django.utils.translation import gettext_lazy as _

class ValueType(models.TextChoices):
    BOOL_VALUE = "BO", _("Bool")
    INT_VALUE = "IN", _("Integer")
    ENUM_VALUE = "EN", _("Eumeration")
