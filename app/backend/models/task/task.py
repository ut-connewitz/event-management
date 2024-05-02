from django.db import models
from django.urls import reverse
from .task_type import TaskType
from .team_restriction import TeamRestriction
from .urgency import Urgency
from .state import State
from backend.models.event import EventDay

class Task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    event_day = models.ForeignKey(EventDay, on_delete=models.CASCADE)
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
    )
    start_time = models.DateTimeField("Beginn", null=True, blank=True)
    finish_time = models.DateTimeField("Ende", null=True, blank=True)
    comment = models.TextField("Kommentar", blank=True)

    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"

    def __str__(self):
        return str(self.event_day)+" "+self.get_task_type_display()

    @property
    def get_html_url(self):
        url = reverse('events_calendar:task_edit', args=(self.task_id,))
        return f'<a href="{url}"> {self.get_task_type_display()} </a>'
