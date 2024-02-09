from django.db import models
from .user import User

class Volunteer(User):
    volunteering_count = models.PositiveIntegerField("Zähler", null=True, blank=True) #not necessary, just a placeholder/example for what this class could be used

    class Meta:
        verbose_name = "Helfer:in"
        verbose_name_plural = "Helfer:innen"

    def __str__(self):
        return str(self.username)
