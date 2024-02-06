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


class UTMember(User):
    member_number = models.PositiveIntegerField("Mitgliedsnummer")

    class Meta:
        verbose_name = "Mitglied"
        verbose_name_plural = "Mitglieder"

    def __str__(self):
        return str(self.username)


class Volunteer(User):
    volunteering_count = models.PositiveIntegerField("Zähler", null=True, blank=True) #not necessary, just a placeholder/example for what this class could be used

    class Meta:
        verbose_name = "Helfer:in"
        verbose_name_plural = "Helfer:innen"

    def __str__(self):
        return str(self.username)

class Adress(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    street = models.CharField("Straße", blank=True, max_length=40)
    house_number = models.CharField("Hausnummer", blank=True, max_length=40)
    postal_code = models.CharField("PLZ", blank=True, max_length=40)
    country = models.CharField("Land", blank=True, max_length=40) #maybe as an option field

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adressen"

    def __str__(self):
        return str(self.username)

class Team(models.Model):
    team_name = models.CharField("Teamname", max_length=40, primary_key=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return str(self.team_name)

class TeamMember(models.Model):
    team_member_id = models.BigAutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Teammitglied"
        verbose_name_plural = "Teammitglieder"

    def __str__(self):
        return str(self.username) + str(self.team_name)
