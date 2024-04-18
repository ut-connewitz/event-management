from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from backend.models.event import Event
from backend.models.user import (User, UTMember, Adress, Team, TeamMember)

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

        ct = ContentType.objects.get_for_model(Event)

        permission_add_event = Permission.objects.create(
            codename='can_add_event',
            name='Can add event',
            content_type=ct
        )

        utadmin_team=Team.objects.get(name="utadmin")
        utadmin_team.permissions.add(permission_add_event)
