from django.db import models
from .act import Act
from .event_day import EventDay
from django.db.utils import IntegrityError
from django.db.models import UniqueConstraint

class EventAct(models.Model):
    event_act_id = models.BigAutoField(primary_key=True)
    event_day = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    act = models.ForeignKey(Act, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["event_day", "act"],
                name="prevent multiple shows by one act at one day constraint",
            ),
        ]
        verbose_name = "Auftritt"
        verbose_name_plural = "Auftritte"

    def __str__(self):
        return str(self.event_day) + " " + str(self.act)

    def save(self, *args, **kwargs):
        try:
            super(EventAct, self).save(*args, **kwargs)
        except IntegrityError:
            print("Dieser Akt spielt bereits an diesem Tag")
            pass
