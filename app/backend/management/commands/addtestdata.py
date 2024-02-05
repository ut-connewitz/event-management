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

        #base and testdate for class user
        utmember1 = UTMember(username="jd", surname="Jane", last_name="Doe", email="jane.doe@mail.de", phone="012345678", member_number="123")
        utmember1.save()
        volunteer1 = Volunteer(username="mm", surname="Max", last_name="Mustermann", email="max@mustermail.net")
        volunteer1.save()
        adress_jd = Adress(username=utmember1, street="Forstweg", house_number="13a", postal_code="43221")
        adress_jd.save()
        team_tontechnik = Team(team_name="Tontecchnik")
        team_tontechnik.save()
        team_lichttechnik = Team(team_name="Lichttechnik")
        team_lichttechnik.save()
        team_küche = Team(team_name= "Küche")
        team_küche.save()
        tontechnik_jd = TeamMember(username=utmember1, team_name=team_tontechnik)
        tontechnik_jd.save()
