from django.db import models

class SettingType(models.TextChoices):
    NOTIFICATION_GLOBAL = "Alle Benachrichtiggungen"
    NOTIFICATION_SPECIFIC = "Eine Benachrichtigung" #not yet implemented, low prio
    APPEARANCE = "Erscheinungsbild"
    MISC_SETTING = "Einstellung"

class ValueType(models.TextChoices):
    BOOL_VALUE = "Bool"
    INT_VALUE = "Integer"
    ENUM_VALUE = "Eumeration"


class Setting(models.Model):
    setting_name = models.CharField(primary_key=True)
    setting_type = models.CharField(
        max_length=30,
        choices=SettingType.choices,
        default=SettingType.MISC_SETTING)
    value_type = models.CharField(
        max_length=15,
        choices=ValueType.choices,
        default=ValueType.BOOL_VALUE)

    class Meta:
        verbose_name = "Einstellung"
        verbose_name_plural = "Einstellungen"

    def __str__(self):
        return self.setting_name

class UserSettingValue(models.Model):
    user_setting_value_id = models.BigAutoField(primary_key=True)
    setting_name = models.ForeignKey(Setting, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Einstellungswert"
        verbose_name_plural = "Einstellungswerte"

    def __str__(self):
        return self.user_setting_value_id

class BoolValue(UserSettingValue):
    bool_value = models.BooleanField()

class IntValue(UserSettingValue):
    int_value = models.BigIntegerField()

class EnumValue(UserSettingValue):
    #TODO
