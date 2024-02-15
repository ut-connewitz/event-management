from django.db import models
from django.contrib import admin
from .user import User

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Helfer:in"
        verbose_name_plural = "Helfer:innen"

    def __str__(self):
        return str(self.username)
