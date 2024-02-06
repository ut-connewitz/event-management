from django.core.management.base import BaseCommand, CommandError
from backend.models import (
User, UTMember, Volunteer, Adress, Team, TeamMember,
Event, EventDay, EventType, Act, EventAct,
Task, Volunteering,
Notification, TaskNotification, VolunteeringNotification,
Setting, UserSettingValue, BoolValue, IntValue, EnumValue
)

class Command(BaseCommand):
    help = "Fügt der Datenbank Testdaten hinzu"

    def handle(self, *args, **options):
        self.stdout.write("running command addtestdata")

        #base and testdata for class user
        utmember1 = UTMember(username="jd", surname="Jane", last_name="Doe", email="jane.doe@mail.de", phone="012345678", member_number="123")
        utmember1.save()
        volunteer1 = Volunteer(username="mm", surname="Max", last_name="Mustermann", email="max@mustermail.net")
        volunteer1.save()
        adress_jd = Adress(username=utmember1, street="Forstweg", house_number="13a", postal_code="43221")
        adress_jd.save()
        team_tontechnik = Team(team_name="Tontechnik") #base data
        team_tontechnik.save()
        team_lichttechnik = Team(team_name="Lichttechnik") #base data
        team_lichttechnik.save()
        team_küche = Team(team_name= "Küche") #base data
        team_küche.save()
        tontechnik_jd = TeamMember(username=utmember1, team_name=team_tontechnik)
        tontechnik_jd.save()

        #base and testdata for event
        event1 = Event(event_name="BAIKALTRAIN DISCO", event_type=EventType.EXTRA, event_description="Disko mit DJ Malhalla und DJ Petrike", event_press="Knackige Tanzmusik vom Balkan bis zum Baikal. \"Von der Eisenbahn in den Club. Die Leute sind nicht zu bremsen.\"") #possibly base data
        event1.save()
        event2 = Event(event_name="JOHNNY & ME", event_type=EventType.CINEMA, event_description="Eine Zeitreise mit Johnny Heartfield")
        event2.save()
