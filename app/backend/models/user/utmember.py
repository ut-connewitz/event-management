from django.db import models
from .user import User

class UTMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_number = models.PositiveIntegerField("Mitgliedsnummer")

    class Meta:
        verbose_name = "Mitglied"
        verbose_name_plural = "Mitglieder"

    def __str__(self):
        return str(self.username)
