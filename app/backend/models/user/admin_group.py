from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group

class AdminGroup(Group):

    class Meta:
        verbose_name = "Admin Gruppe"
        verbose_name_plural = "Admin Gruppen"
        proxy = True

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        try:
            super(AdminGroup, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass
