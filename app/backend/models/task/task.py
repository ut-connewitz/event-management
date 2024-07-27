from django.db import models
from django.urls import reverse
from django.db.utils import IntegrityError
from .task_type import TaskType
from .team_restriction import TeamRestriction
from .urgency import Urgency
from .state import State
from backend.models.event import Event

class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name = "Veranstaltung",
        )
    task_type = models.CharField(
        "Aufgabenart",
        max_length=2,
        choices=TaskType.choices,
        default=TaskType.OTHER,
    )
    team_restriction = models.CharField(
        "Teambindung",
        max_length=2,
        choices=TeamRestriction.choices,
        default=TeamRestriction.NONE,
    )
    urgency = models.CharField(
        "Dringlichkeit",
        max_length=2,
        choices=Urgency.choices,
        default=Urgency.MEDIUM,
    )
    state = models.CharField(
        "Status",
        max_length=2,
        choices=State.choices,
        default=State.FREE,
        editable=False,
        # this is to avoid triggering unwanted db behavoiour by manually setting a Task.State
        # Task.States can now only be set by confirming to / stepping back from a Volunteering
    )
    start_time = models.TimeField(
        "Beginn",
        null=True,
        blank=True,
    )
    finish_time = models.TimeField(
        "Ende",
        null=True,
        blank=True,
    )
    comment = models.TextField(
        "Kommentar",
        blank=True,
    )

    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"
        order_with_respect_to = "event"

    def __str__(self):
        return str(self.event)+" "+self.get_task_type_display()

    def save(self, *args, **kwargs):
        try:
            super(Task, self).save(*args, **kwargs)
            #self.check_state_change()
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass

    @property
    def get_html_url(self):
        url = reverse('events_calendar:task_edit', args=(self.task_id,))
        return f'<a href="{url}"> {self.get_task_type_display()} </a>'

    #def check_state_change(self):
    #    if self.state != State.FREE:
    #        self.deletedvolunteering_set.clear()
    # unfortunately it is not possible to delete the DeletedVolunteering with foreign key to its Task instance here
    # this self.deletedvolunteering_set.clear() just dissolves the foreign key connection between the task instance and the (all) connected DeletedVolunteerings
    # and the clear() call is only possible if on_delete=models.SET_NULL is chosen in the DeletedVolunteering model
    # the update() method of the DeletedVolunteering then is triggered, not the save method
    # it seems not possible to trigger a self.delete() of the deleted volunteering instance there either
    # due to circular dependency error it is also not possible to include DeletedVolunteering here, search for the instance and delete it
    # because the Task class is already included in the DeletedVolunteering class to make the foreign key possible
    # https://docs.djangoproject.com/en/4.2/ref/models/relations/
    # https://docs.djangoproject.com/en/4.2/ref/models/querysets/
    # since all this was meant to avoid unwanted db behavior in case someone manually sets a tasks state to TAKEN while there is still a connected deleted volunteering
    # the easiest way to avoid this seems to be just to disallow manually setting task states at all, what would make sense anyways
