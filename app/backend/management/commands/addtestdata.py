from django.core.management.base import BaseCommand, CommandError
from backend.models import (
User, UTMember, Volunteer, Adress, Team, TeamMember,
Event, EventDay, Act, EventAct,
Task, Volunteering,
Notification, TaskNotification, VolunteeringNotification,
Setting, UserSettingValue, BoolValue, IntValue, EnumValue
)

class Command(BaseCommand):
    help = "Fügt der Datenbank Testdaten hinzu"

    def handle(self, *args, **options):
        self.stdout.write("running command addtestdata")
