from django.db import models
from .notification import Notification
from backend.models.task import Task

class TaskNotification(Notification):
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Aufgabenbenachrichtigung"
        verbose_name_plural = "Aufgabenbenachrichtigungen"
