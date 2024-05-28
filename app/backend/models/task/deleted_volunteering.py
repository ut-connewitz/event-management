import logging
from django.db import models
from django.db.utils import IntegrityError
from .task import Task, State
from backend.models.user import User

class DeletedVolunteeringQuerySet(models.QuerySet):
    def update(self, *args, **kwargs):
        logger = logging.getLogger(__name__)
        for object in self:
            logger.error("updating")
            #object.apply_task_state
            if object.task == None:
                object.delete()

        super().update(*args, **kwargs)

class DeletedVolunteeringManager(models.Manager):
    def get_queryset(self):
        return DeletedVolunteeringQuerySet(model=self.model, using=self._db, hints=self._hints)

class DeletedVolunteering(models.Model):
    task = models.ForeignKey(
        Task,
        null=True,
        on_delete=models.CASCADE,
        verbose_name = "Aufgabe",
    )
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name = "Person",
    )

    timestamp = models.DateTimeField("Zeitpunkt", null=False, blank=False)

    comment = models.TextField("Kommentar", blank=True, max_length=300)

    objects = DeletedVolunteeringManager()


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
            self.apply_task_state
            super(DeletedVolunteering, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass

    def apply_task_state(self):
        logger = logging.getLogger(__name__)
        logger.info("applying task state")
        if self.task == None:
            self.delete()
