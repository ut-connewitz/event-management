from django.db import models
from .user_setting_value import UserSettingValue

class EnumValue(UserSettingValue):
    #TODO

    class Meta:
        verbose_name = "Enumwert"
        verbose_name_plural ="Enumwerte"
