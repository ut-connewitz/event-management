from django.db import models

class Act(models.Model):
    act_name = models.CharField(
        "Aktname",
        max_length=40,
        primary_key=True
    )
    person_count = models.PositiveIntegerField("Personenzahl", null=True, blank=True)
    act_image = models.ImageField("Bild", null=True, blank=True)
    #TODO: test options for music files
    music_sample = models.FileField("Musikbeispiel", null=True, blank=True)
    diet = models.CharField("Ernährung", blank=True, max_length=100)
    act_email = models.EmailField("Email", null=True, blank=True, max_length=100)
    act_phone = models.CharField("Telefon", blank=True, max_length=15)

    class Meta:
        verbose_name = "Ensemble"
        verbose_name_plural = "Ensembles"

    def __str__(self):
        return str(self.act_name)
