from django.db import models
from backend.models.user.user import User
from .setting import Setting

class UserSettingValue(models.Model):
    user_setting_value_id = models.BigAutoField(primary_key=True)
    setting_name = models.ForeignKey(Setting, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Einstellungswert"
        verbose_name_plural = "Einstellungswerte"

    def __str__(self):
        return str(self.username) + " " + str(self.setting_name)
