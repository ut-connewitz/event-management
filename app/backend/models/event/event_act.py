from django.db import models
from .act import Act
from .event_day import EventDay

class EventAct(models.Model):
    event_act_id = models.BigAutoField(primary_key=True)
    event_day = models.ForeignKey(EventDay, on_delete=models.CASCADE)
    act_name = models.ForeignKey(Act, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Auftritt"
        verbose_name_plural = "Auftritte"

    def __str__(self):
        return str(self.event_day) + " " + str(self.act_name)
