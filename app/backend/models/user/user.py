from django.db import models
from .team import Team

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
from django.urls import reverse

class User(AbstractUser):
    phone = models.CharField("Telefon", blank=True, max_length=20)

    groups = models.ManyToManyField(
        Team,
        blank = True,
        help_text=_("Teams zu welchen die Person gehört. Alle Befugnisse einer Gruppe gehen auf die Person über"),
        related_name = "user_set",
        related_query_name = "user",
        through="TeamMember"
    )

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        app_label = "backend"

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        try:
            super(User, self).save(*args, **kwargs)
        except IntegrityError:
            print("Username ist bereits vergeben")
            pass

    def get_absolute_url(self):
        return reverse("profile:account", kwargs={"pk": self.pk})

    @property
    def get_html_url(self):
        url = reverse('profile:account', args=(self.pk,))
        return f'<a href="{url}"> {self.username} </a>'


# TeamMember class is placed here within the .user file in order to avoid circular dependencies during app initialisation
# preferred option would be to have this within an own file like all other model classes
# but since User class tries to import TeamMember in the through="TeamMember" field
# and TeamMember tries to import User in the user field, a circular dependency error is thrown

# to overwrite the delete() method (or any method) for SQL queries the QuerySet must be adjusted
# this is necessary for bulk operations like when using list operations via the admin panel
class TeamMemberQuerySet(models.QuerySet):
    # this delete method is triggered, when multiple objects are deleted (e.g via TeamMember list in admin panel)
    def delete(self):
        for object in self:
            if object.team.name == "UT-Admin":
                user = object.user
                user.is_staff = False
                user.save()
        return super().delete()

class TeamMemberManager(models.Manager):
    def get_queryset(self):
        return TeamMemberQuerySet(model=self.model, using=self._db, hints=self._hints)


class TeamMember(models.Model):
    team_member_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    objects = TeamMemberManager()

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=["user", "team"], name="prevent multiple memberships of one person in one team constraint")
        ]
        verbose_name = "Teammitgliedschaft"
        verbose_name_plural = "Teammitgliedschaften"

    def __str__(self):
        return str(self.team) + " " + str(self.user)

    # overwrite save methods with caution!
    # this is meant to prevent db crash if one person is added to the same team more than once from addtestdata.py
    # this may occur, when addtestdata.py is run multiple times for development/testing reasons
    # for now, only unique fields are problematic since primary key duplicates just wont be inserted (as expected) without crashing the db
    # exception handling in the admin panel is not affected
    def save(self, *args, **kwargs):
        try:
            super(TeamMember, self).save(*args, **kwargs)
            self.set_user_is_staff()
        except IntegrityError:
            print("Person ist bereits in diesem Team")
            pass

    # this delete method is triggered, when one single object is deleted (e.g. while editing teammembership of a single user)
    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        if not user.groups.filter(name="UT-Admin"):
            user.is_staff = False
            user.save()

    def set_user_is_staff(self):
        if self.user.groups.filter(name="UT-Admin"):
            self.user.is_staff = True
            self.user.save()
