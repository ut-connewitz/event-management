from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group

class Team(Group):
    #group = models.OneToOneField(Group, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        proxy = True

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        try:
            super(Team, self).save(*args, **kwargs)
        except IntegrityError:
            print("Team ist bereits vorhanden")
            pass
