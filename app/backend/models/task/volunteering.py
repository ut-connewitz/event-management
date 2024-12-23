from datetime import datetime
import logging

from django.db import models
from django.db.utils import IntegrityError
from django.utils.timezone import get_current_timezone
from .confirmation_type import ConfirmationType
from .task import Task, State
from .deleted_volunteering import DeletedVolunteering
from backend.models.user import User

# to overwrite the delete() method (or any method) for SQL queries the QuerySet must be adjusted
# this is necessary for bulk operations like when using list operations via the admin panel
class VolunteeringQuerySet(models.QuerySet):
    def delete(self):
        for object in self:
            task = object.task
            task.state = State.FREE
            task.save()
        return super().delete()

class VolunteeringManager(models.Manager):
    def get_queryset(self):
        return VolunteeringQuerySet(model=self.model, using=self._db, hints=self._hints)

class Volunteering(models.Model):
    volunteering_id = models.BigAutoField(primary_key=True)
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
    confirmation_type = models.CharField(
        "Zusage",
        max_length=15,
        choices=ConfirmationType.choices,
        default=ConfirmationType.YES,
    )
    comment = models.TextField(
        "Kommentar",
        blank=True,
        max_length=800,
    )

    objects = VolunteeringManager()

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=["task"], name="prevent multiple volunteerings for one task constraint")
        ]
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"
        order_with_respect_to = "task"

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
        task = self.task
        task.state = State.FREE
        task.save()
        super().delete(*args, **kwargs)

    def confirmation_type_change(self):
        if self.confirmation_type == ConfirmationType.NO:
            timestamp = datetime.now(tz=get_current_timezone())
            deleted_instance = DeletedVolunteering.objects.create(
                task = self.task,
                user = self.user,
                timestamp = timestamp,
                comment = self.comment,
            )
            deleted_instance.save()
            #logger = logging.getLogger(__name__) #debug
            #logger.error('this is not an error') #debug
            self.delete()
        elif self.confirmation_type == ConfirmationType.YES:
            self.task.state = State.TAKEN
            try:
                deleted_instance = DeletedVolunteering.objects.get(task=self.task)
            except DeletedVolunteering.DoesNotExist:
                deleted_instance = None
            if deleted_instance != None:
                deleted_instance.delete()
            self.task.save()
