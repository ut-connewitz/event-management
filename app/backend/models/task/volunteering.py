from django.db import models
from django.db.utils import IntegrityError
from .confirmation_type import ConfirmationType
from .task import Task, State
from backend.models.user import User

class VolunteeringQuerySet(models.QuerySet):
    def delete(self):
        print("deleting queryset")
        return super().delete()

class VolunteeringManager(models.Manager):
    def get_queryset(self):
        return VolunteeringQuerySet(model=self.model, using=self._db, hints=self._hints)

class Volunteering(models.Model):
    volunteering_id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_type = models.CharField(
        "Zusage",
        max_length=15,
        choices=ConfirmationType.choices,
        default=ConfirmationType.YES,
    )
    comment = models.TextField("Kommentar", blank=True, max_length=300)

    objects = VolunteeringManager()

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=["task"], name="prevent multiple volunteerings for one task constraint")
        ]
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"

    def __str__(self):
        return str(self.user) + " " + str(self.task)

    def save(self, *args, **kwargs):
        try:
            super(Volunteering, self).save(*args, **kwargs)
            self.confirmation_type_change()
        except IntegrityError:
            print("Dienst ist bereits übernommen")
            pass

    def delete(self, *args, **kwargs):
        self.task.state = State.FREE
        self.task.save()
        super().delete(*args, **kwargs)

    def confirmation_type_change(self):
        if self.confirmation_type == ConfirmationType.NO:
            self.delete()
        elif self.confirmation_type == ConfirmationType.YES:
            self.task.state = State.TAKEN
            self.task.save()
