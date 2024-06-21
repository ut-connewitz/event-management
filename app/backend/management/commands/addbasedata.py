from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from backend.models.event import (EventSeries, Act, Event, EventType)
from backend.models.task import (Task, ConfirmationType, State, TaskType, TeamRestriction, Urgency, Volunteering)
from backend.models.user import (User, UTMember, Adress, Team, TeamMember)
from backend import models
from django.db.utils import IntegrityError

TEAM_PERMISSIONS = {
    'utadmin':{
        models.event.EventSeries: ['add', 'change', 'delete', 'view'],
        models.event.Act: ['add', 'change', 'delete', 'view'],
        models.event.Event: ['add', 'change', 'delete', 'view'],
        models.task.Task: ['add', 'change', 'delete', 'view'],
        models.task.Volunteering: ['add', 'change', 'delete', 'view'],
        models.user.Adress: ['add', 'change', 'delete', 'view'],
        models.user.TeamMember: ['add', 'change', 'delete', 'view'],
        models.user.Team: ['view'],
        models.user.User: ['add', 'change', 'delete', 'view'],
        models.user.UTMember: ['add', 'change', 'delete', 'view'],
    }
}

class Command(BaseCommand):
    help = "Fügt der Datenbank Basisdaten hinzu"

    def handle(self, *args, **options):
        self.stdout.write("running command addtestdata")

        team1 = Team.objects.create(name="utadmin")
        team1.save()
        team2 = Team.objects.create(name="küche")
        team2.save()
        team3 = Team.objects.create(name="lichttechnik")
        team3.save()
        team4 = Team.objects.create(name="tontechnik")
        team4.save()

        #ct = ContentType.objects.get_for_model(EventSeries)

        #permission_add_eventseries = Permission.objects.create(
        #    codename='can_add_eventseries',
        #    name='Can add eventseries',
        #    content_type=ct
        #)

        #utadmin_team=Team.objects.get(name="utadmin")
        #utadmin_team.permissions.add(permission_add_eventseries)

        #
        for team_name in TEAM_PERMISSIONS:
            team, created = Team.objects.get_or_create(name=team_name)
            for model_cls in TEAM_PERMISSIONS[team_name]:
                for permission_index, permission_name in \
                        enumerate(TEAM_PERMISSIONS[team_name][model_cls]):

                    #generate permission name as Django would generate it
                    #print("try adding "+permission_name + "_" + model_cls._meta.model_name) #debug
                    codename = permission_name + "_" + model_cls._meta.model_name

                    try:
                        content_type = ContentType.objects.get(app_label='backend', model=model_cls._meta.model_name)
                        permission = Permission.objects.get(codename=codename, content_type=content_type)
                        team.permissions.add(permission)
                        self.stdout.write("Adding "+codename+" to group "+team.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
                    except IntegrityError as e:
                        error_message = e.__cause__
                        print(error_message)
                        pass
