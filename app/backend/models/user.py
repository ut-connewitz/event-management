from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=true)
    password = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"

    def __str__(self):
        return self.username


class UTMember(User):
    member_number = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Mitglied"

    def __str__(self):
        return self.username


class Volunteer(User):
    volunteering_count = models.PositiveIntegerField()

    def __str__(self):
        return self.username

class Adress(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=40)
    house_number = models.CharField(max_length=40)
    postal_code = models.CharField(max_length=40)
    country = models.CharField(max_length=40)

    class Meta:
        verbose_name = "Adresse"

    def __str__(self):
        return self.username

class Team(models.Model):
    team_name = models.CharField(max_length=40, primary_key=true)

    class Meta:
        verbose_name = "Team"

    def __str__(self):
        return self.team_name

class TeamMember(models.Model):
    team_member_id = models.BigAutoField(primary_key=true)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Team Member"

    def __str__(self):
        return self.username + self.team_name
