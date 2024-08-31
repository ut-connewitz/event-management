from django.db import models
from django.db.utils import IntegrityError

class Act(models.Model):
    act_id = models.BigAutoField(primary_key=True)
    act_name = models.CharField(
        "Name",
        max_length=40,
    )
    person_count = models.PositiveIntegerField(
        "Personenzahl",
        null=True,
        blank=True,
    )
    act_image = models.ImageField(
        "Bild",
        null=True,
        blank=True,
    )
    #TODO: test options for music files
    music_sample = models.FileField(
        "Musikbeispiel",
        null=True,
        blank=True,
    )
    diet = models.CharField(
        "Ernährung",
        blank=True,
        max_length=400,
    )
    act_email = models.EmailField(
        "Email",
        null=True,
        blank=True,
        max_length=100)
    act_phone = models.CharField(
        "Telefon",
        blank=True,
        max_length=15,
    )

    class Meta:
        verbose_name = "Ensemble"
        verbose_name_plural = "Ensembles"
        constraints = [
            models.UniqueConstraint(fields=["act_name"], name="prevent Act name duplicates constraint")
        ]

    def save(self, *args, **kwargs):
        try:
            super(Act, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass

    def __str__(self):
        return str(self.act_name)
