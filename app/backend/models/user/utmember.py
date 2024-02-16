from django.db import models
from .user import User
from django.db.utils import IntegrityError

class UTMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_number = models.PositiveIntegerField("Mitgliedsnummer")

    class Meta:
        verbose_name = "Mitglied"
        verbose_name_plural = "Mitglieder"

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        try:
            super(UTMember, self).save(*args, **kwargs)
        except IntegrityError:
            print("Person ist bereits als Mitglied eingetragen")
            pass
