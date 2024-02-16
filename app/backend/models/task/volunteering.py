from django.db import models
from .confirmation_type import ConfirmationType
from .task import Task
from backend.models.user import User

class Volunteering(models.Model):
    volunteering_id = models.BigAutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmation_type = models.CharField(
        "Art der Zusage",
        max_length=15,
        choices=ConfirmationType.choices,
        default=ConfirmationType.NOT,
    )

    class Meta:
        verbose_name = "Dienst"
        verbose_name_plural = "Dienste"

    def __str__(self):
        return str(self.user) + " " + str(self.task)
