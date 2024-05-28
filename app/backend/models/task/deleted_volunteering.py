from django.db import models
from django.db.utils import IntegrityError
from .task import Task, State
from backend.models.user import User

class DeletedVolunteering(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name = "Aufgabe",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = "Person",
    )

    timestamp = models.DateTimeField("Zeitpunkt", null=False, blank=False)

    comment = models.TextField("Kommentar", blank=True, max_length=300)


    class Meta:
        constraints = [
        models.UniqueConstraint(fields=["task"], name="prevent multiple deletd volunteerings for one task constraint")
        ]
        verbose_name = "Gelöschter Dienst"
        verbose_name_plural = "Gelöschte Dienste"

    def __str__(self):
        return str(self.user) + " " + str(self.task)

    def save(self, *args, **kwargs):
        try:
            super(DeletedVolunteering, self).save(*args, **kwargs)
        except IntegrityError:
            print("Objekt ist bereits vorhanden")
            pass
