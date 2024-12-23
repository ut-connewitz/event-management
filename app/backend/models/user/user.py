from django.db import models
from .team import Team
from .admin_group import AdminGroup

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
from django.urls import reverse

# custom manager for overwriting the create_user and create_superuser methods
# in the current state there is no practical difference to the default methods
# but having this setup make possible future customisations (e.g using email instead of username) easier
class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username erforderlich")

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Username erforderlich")

        #for k, v in extra_fields.items(): #debug
        #    print(k, v)

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        for k, v in extra_fields.items(): #debug
            print(k, v)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    phone = models.CharField("Telefon", blank=True, max_length=20)

    groups = models.ManyToManyField(
        AdminGroup,
        blank = True,
        help_text=_("Administrative Gruppe, zu welcher diese Person gehört. Alle Befugnisse einer Gruppe gehen auf die Person über"),
        related_name = "user_set",
        related_query_name = "user",
        through="AdminGroupMember"
    )

    teams = models.ManyToManyField(
        Team,
        blank = True,
        help_text=_("Team, zu welcher diese Person gehört."),
        related_name = "user_set",
        related_query_name = "user",
        through="TeamMember"
    )

    objects = UserManager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        app_label = "backend"

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        try:
            super(User, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass

    def get_absolute_url(self):
        return reverse("profile:account", kwargs={"pk": self.pk})

    @property
    def get_html_url(self):
        url = reverse('profile:account', args=(self.pk,))
        return f'<a href="{url}"> {self.username} </a>'


# AdminGroupMember and TeamMember classes are placed here within the .user file in order to avoid circular dependencies during app initialisation
# preferred option would be to have this within an own file like all other model classes
# but since User class tries to import AdminGroupMember/TeamMember in the "through" field
# and AdminGroupMember/TeamMember tries to import User in the user field, a circular dependency error is thrown

# to overwrite the delete() method (or any method) for SQL queries the QuerySet must be adjusted
# this is necessary for bulk operations like when using list operations via the admin panel
class AdminGroupMemberQuerySet(models.QuerySet):
    def create(self, *args, **kwargs):
        user = kwargs["user"]
        admin_group = kwargs["admin_group"]
        if admin_group.name == "Veranstaltungsorganisation":
            user.is_staff=True
            user.save()
        return super().create(*args, **kwargs)


    # this delete method is triggered, when multiple objects are deleted (e.g via TeamMember list in admin panel)
    def delete(self):
        for object in self:
            # print("bulk deleting team membership " +str(object.user)+str(object.team)) #debug
            if object.admin_group.name == "Veranstaltungsorganisation":
                user = object.user
                if user.is_superuser == False: #superusers should not be affected by this
                    # print("bulk deleting team membership setting is_staff" +str(user)+str(object.team)) #debug
                    user.is_staff = False
                    # print("bulk deleting team membership setting is_staff" +str(user.is_staff)) #debug
                    user.save()
            # print("bulk deleting team membership" +str(user.is_staff)) #debug
        return super().delete()

    def update(self, *args, **kwargs):
        #print("updating") #debug
        super().update(*args, **kwargs)
        for object in self:
            #print("setting" + str(object)) #debug
            if object.admin_group.name == "Veranstaltungsorganisation":
                object.set_user_is_staff()

class AdminGroupMemberManager(models.Manager):
    def get_queryset(self):
        return AdminGroupMemberQuerySet(model=self.model, using=self._db, hints=self._hints)


class AdminGroupMember(models.Model):
    admin_group_member_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = "Person",
    )
    admin_group = models.ForeignKey(
        AdminGroup,
        on_delete=models.CASCADE,
        verbose_name = "Admin Gruppe",
    )
    objects = AdminGroupMemberManager()

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=["user", "admin_group"], name="prevent multiple memberships of one person in one admin group constraint")
        ]
        verbose_name = "Admins"
        verbose_name_plural = "Admins"

#  __init__() is called on python object instantiation, not on creation of db records
#    def __init__(self, *args, **kwargs):
#        super(TeamMember, self).__init__(*args, **kwargs)
#        try:
#            if self.team.name == "UT-Admin":
#                self.user.is_staff = True
#        except Team.DoesNotExist:
#            pass

    def __str__(self):
        return str(self.admin_group) + " " + str(self.user)

    # this is meant to prevent db crash if one person is added to the same team more than once from addtestdata.py
    # this may occur, when addtestdata.py is run multiple times for development/testing reasons
    # for now, only unique fields are problematic since primary key duplicates just wont be inserted (as expected) without crashing the db
    # exception handling in the admin panel is not affected
    def save(self, *args, **kwargs):
        try:
            # print("saving") #debug
            super(AdminGroupMember, self).save(*args, **kwargs)
            self.set_user_is_staff()
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass

    # this delete method is triggered, when one single object is deleted (e.g. while editing teammembership of a single user)
    def delete(self, *args, **kwargs):
        user = self.user
        # print("instance deleting team membership " +str(user)+str(self.team)) #debug
        super().delete(*args, **kwargs)
        user.refresh_from_db()
        if (
                not user.groups.filter(name="Veranstaltungsorganisation")
                and user.is_superuser == False #superusers should not be affected by this
        ):
            user.is_staff = False
            user.save()

    def set_user_is_staff(self):
        if self.user.groups.filter(name="Veranstaltungsorganisation"):
            self.user.is_staff = True
            self.user.save()



class TeamMember(models.Model):
    team_member_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name = "Person",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name = "Team",
    )

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=["user", "team"], name="prevent multiple memberships of one person in one team constraint")
        ]
        verbose_name = "Teammitgliedschaft"
        verbose_name_plural = "Teammitgliedschaften"

    def __str__(self):
        return str(self.team) + " " + str(self.user)

    def save(self, *args, **kwargs):
        try:
            super(TeamMember, self).save(*args, **kwargs)
        except IntegrityError as e:
            error_message = e.__cause__
            print(error_message)
            pass
