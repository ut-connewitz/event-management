from django.db import models
from django.contrib import admin
from .user import User
from django.db.utils import IntegrityError

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Helfer:in"
        verbose_name_plural = "Helfer:innen"

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        try:
            super(Volunteer, self).save(*args, **kwargs)
        except IntegrityError:
            print("Person ist bereits als Helfer:in eingetragen")
            pass
