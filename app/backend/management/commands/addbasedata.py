from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from backend.models.event import (EventSeries, Act, Event, EventType, PastEvent, Location)
from backend.models.task import (Task, ConfirmationType, State, TaskType, TeamRestriction, Urgency, Volunteering)
from backend.models.user import (AdminGroup, AdminGroupMember, User, UTMember, Adress, Team, TeamMember)
from backend import models
from django.db.utils import IntegrityError

ADMIN_GROUP_PERMISSIONS = {
    'Veranstaltungsorganisation':{
        models.event.EventSeries: ['add', 'change', 'view'],
        models.event.Act: ['add', 'change', 'delete', 'view'],
        models.event.Event: ['add', 'change', 'delete', 'view'],
        models.event.Location: ['add', 'change', 'view'],
        models.event.PastEvent: ['change', 'view'],
        models.task.Task: ['add', 'change', 'delete', 'view'],
        models.task.Volunteering: ['add', 'change', 'delete', 'view'],
        models.user.Adress: ['add', 'change', 'delete', 'view'],
        models.user.TeamMember: ['add', 'change', 'delete', 'view'],
        models.user.Team: ['view'],
        models.user.AdminGroupMember: ['view'],
        models.user.User: ['add', 'change', 'view'],
        models.user.UTMember: ['add', 'change', 'delete', 'view'],
    }
}

class Command(BaseCommand):
    help = "Fügt der Datenbank Basisdaten hinzu"

    def handle(self, *args, **options):
        self.stdout.write("running command addtestdata")

        admin_group1 = AdminGroup.objects.create(name="Veranstaltungsorganisation")
        admin_group1.save()
        team1 = Team.objects.create(name="Küche")
        team1.save()
        team2 = Team.objects.create(name="Licht")
        team2.save()
        team3 = Team.objects.create(name="Ton")
        team3.save()
        team4 = Team.objects.create(name="Verwaltung")
        team4.save()

        self.assign_admin_group_permissions()

    def assign_admin_group_permissions(self):
        for admin_group_name in ADMIN_GROUP_PERMISSIONS:
            admin_group, created = AdminGroup.objects.get_or_create(name=admin_group_name)
            for model_cls in ADMIN_GROUP_PERMISSIONS[admin_group_name]:
                for permission_index, permission_name in \
                        enumerate(ADMIN_GROUP_PERMISSIONS[admin_group_name][model_cls]):

                    #generate permission name as Django would generate it
                    #print("try adding "+permission_name + "_" + model_cls._meta.model_name) #debug
                    codename = permission_name + "_" + model_cls._meta.model_name

                    try:
                        content_type = ContentType.objects.get(app_label='backend', model=model_cls._meta.model_name)
                        permission = Permission.objects.get(codename=codename, content_type=content_type)
                        admin_group.permissions.add(permission)
                        self.stdout.write("Adding "+codename+" to admin group "+admin_group.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
                    except IntegrityError as e:
                        error_message = e.__cause__
                        print(error_message)
                        pass
