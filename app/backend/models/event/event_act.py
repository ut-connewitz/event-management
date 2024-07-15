from django.db import models
from .act import Act
from .event import Event
from django.db.utils import IntegrityError
from django.db.models import UniqueConstraint

class EventAct(models.Model):
    event_act_id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name = "Veranstaltung",
    )
    act = models.ForeignKey(
        Act,
        on_delete=models.CASCADE,
        verbose_name = "Ensemble",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["event", "act"],
                name="prevent multiple shows by one act at one event constraint",
            ),
        ]
        verbose_name = "Auftritt"
        verbose_name_plural = "Auftritte"

    def __str__(self):
        return str(self.event) + " " + str(self.act)

    def save(self, *args, **kwargs):
        try:
            super(EventAct, self).save(*args, **kwargs)
        except IntegrityError:
            print("Dieser Akt spielt bereits an diesem Tag")
            pass
