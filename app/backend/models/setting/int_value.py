from django.db import models
from .user_setting_value import UserSettingValue

class IntValue(UserSettingValue):
    int_value = models.BigIntegerField()

    class Meta:
        verbose_name = "Integerwert"
        verbose_name_plural = "Integerwerte"
