from django.db import models

class SettingType(models.TextChoices):
    NOTIFICATION_GLOBAL = "NG", _("Einstellung für alle Benachrichtiggungen")
    NOTIFICATION_SPECIFIC = "NS", _("Einstellung für eine Benachrichtigung") #not yet implemented, low prio
    APPEARANCE = "AP", _("Erscheinungsbild")
    MISC_SETTING = "MS", _("Einstellung")

class ValueType(models.TextChoices):
    BOOL_VALUE = "BO", _("Bool")
    INT_VALUE = "IN", _("Integer")
    ENUM_VALUE = "EN", _("Eumeration")


class Setting(models.Model):
    setting_name = models.CharField(primary_key=true)
    setting_type = models.CharField(
        max_length=2,
        choices=SettingType.choices
        default=SettingType.MISC_SETTING)
    value_type = models.CharField(
        max_length=2,
        choices=ValueType.choices
        default=ValueType.BOOL_VALUE)

    class Meta:
        verbose_name = "Einstellung"
        verbose_name_plural = "Einstellungen"

    def __str__(self):
        return self.setting_name

class UserSettingValue(models.Model):
    user_setting_value_id = models.BigAutoField(primary_key=true)
    setting_name = models.ForeignKey(Setting, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

class BoolValue(UserSettingValue):
    bool_value = models.BooleanField()

class IntValue(UserSettingValue):
    int_value = models.BigIntegerField()

class EnumValue(UserSettingValue):
    #TODO
