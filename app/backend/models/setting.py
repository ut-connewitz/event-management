from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User

class SettingType(models.TextChoices):
    NOTIFICATION_GLOBAL = "NG", _("Benachrichtigungen allgmein")
    NOTIFICATION_SPECIFIC = "NS", _("Bestimmte Benachrichtigung") #not yet implemented, low prio
    APPEARANCE = "AP", _("Erscheinungsbild")
    MISC_SETTING = "ST", _("Einstellung")

class ValueType(models.TextChoices):
    BOOL_VALUE = "BO", _("Bool")
    INT_VALUE = "IN", _("Integer")
    ENUM_VALUE = "EN", _("Eumeration")

class Setting(models.Model):
    setting_name = models.CharField("Einstellungsname", primary_key=True)
    setting_type = models.CharField(
        "Einstellungsart",
        max_length=2,
        choices=SettingType.choices,
        default=SettingType.MISC_SETTING,
    )
    value_type = models.CharField(
        "Datentyp",
        max_length=2,
        choices=ValueType.choices,
        default=ValueType.BOOL_VALUE,
    )

    class Meta:
        verbose_name = "Einstellung"
        verbose_name_plural = "Einstellungen"

    def __str__(self):
        return str(self.setting_name)

class UserSettingValue(models.Model):
    user_setting_value_id = models.BigAutoField(primary_key=True)
    setting_name = models.ForeignKey(Setting, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Einstellungswert"
        verbose_name_plural = "Einstellungswerte"

    def __str__(self):
        return str(self.user_setting_value_id)

class BoolValue(UserSettingValue):
    bool_value = models.BooleanField()

    class Meta:
        verbose_name = "Boolwert"
        verbose_name_plural = "Boolwerte"

class IntValue(UserSettingValue):
    int_value = models.BigIntegerField()

    class Meta:
        verbose_name = "Integerwert"
        verbose_name_plural = "Integerwerte"

class EnumValue(UserSettingValue):
    #TODO

    class Meta:
        verbose_name = "Enumwert"
        verbose_name_plural ="Enumwerte"
