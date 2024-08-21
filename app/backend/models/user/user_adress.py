from django.db import models
from django.db.utils import IntegrityError
from django.urls import reverse
from .user import User
from backend.models.misc import Adress

class UserAdress(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name = "Person",
    )
    adress = models.ForeignKey(
        Adress,
        on_delete=models.CASCADE,
        verbose_name = "Adresse",
    )
     #maybe as an option field

    class Meta:
        verbose_name = "Anschrift"
        verbose_name_plural = "Anschriften"
        constraints = [
            models.UniqueConstraint(fields=["user", "adress"], name="prevent UserAdress duplicates constraint")
        ]


    def __str__(self):
        return "Anschrift von "+ str(self.user)

    def save(self, *args, **kwargs):
        try:
            super(UserAdress, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass
