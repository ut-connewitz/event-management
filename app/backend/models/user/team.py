from django.db import models
from django.db.utils import IntegrityError

class Team(models.Model):
    name = models.CharField("Teamname", blank=False, max_length=40)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        try:
            super(Team, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass
