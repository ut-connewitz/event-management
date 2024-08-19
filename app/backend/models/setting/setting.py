from django.db import models
from .setting_type import SettingType
from .value_type import ValueType


class Setting(models.Model):
    setting_id = models.BigAutoField(primary_key=True)
    setting_name = models.CharField(
        "Einstellungsname",
        max_length=50,
    )
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
