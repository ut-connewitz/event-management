from django.db import models
from .user_setting_value import UserSettingValue

class BoolValue(UserSettingValue):
    bool_value = models.BooleanField()

    class Meta:
        verbose_name = "Boolwert"
        verbose_name_plural = "Boolwerte"
