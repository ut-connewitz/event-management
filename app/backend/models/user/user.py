from django.db import models

class User(models.Model):
    username = models.CharField("Anmeldename", max_length=20, primary_key=True)
    surname = models.CharField("Vorname", blank=True, max_length=40)
    last_name = models.CharField("Nachname", blank=True, max_length=40)
    email = models.EmailField("Email", null=True, blank=True, max_length=100)
    phone = models.CharField("Telefon", blank=True, max_length=20)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"

    def __str__(self):
        return str(self.username)
