from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime, parse_duration
from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import Group, Permission
from backend.models.setting import (Setting, UserSettingValue, BoolValue, IntValue, EnumValue)
from backend.models.user import (User, UTMember, Volunteer, Adress)
from backend.models.event import(EventType, Event, EventDay, Act, EventAct)
from backend.models.notification import (NotificationType, Notification, TaskNotification, VolunteeringNotification)
from backend.models.task import (TaskType, TeamRestriction, Urgency, State, Task, ConfirmationType, Volunteering)

class Command(BaseCommand):
    help = "Fügt der Datenbank Testdaten hinzu"

    def handle(self, *args, **options):
        self.stdout.write("running command addtestdata")

        #group1 = Group.objects.create(name="utadmin")
        #group1.save()
        #group2 = Group.objects.create(name="küche")
        #group2.save()
        group3 = Group.objects.create(name="lichttechnik")
        group3.save()
        group4 = Group.objects.create(name="tontechnik")
        group4.save()

        #base and testdata for class user
        utmember1 = UTMember(
            username="jd",
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@mail.de",
            member_number="123",
        )
        utmember1.set_password('lazy1234')
        utmember1.save()
        volunteer1 = Volunteer(
            username="mm",
            first_name="Max",
            last_name="Mustermann",
            email="max@mustermail.net",
        )
        volunteer1.set_password("lazy1234")
        volunteer1.save()
        adress_jd = Adress(
            username=utmember1,
            street="Forstweg",
            house_number="13a",
            postal_code="43221",
        )
        adress_jd.save()



        #base and testdata for event
        event1 = Event(
            event_name="BAIKALTRAIN DISCO",
            event_type=EventType.EXTRA,
            event_description="Disko mit DJ Malhalla und DJ Petrike",
            event_press="Knackige Tanzmusik vom Balkan bis zum Baikal. \"Von der Eisenbahn in den Club. Die Leute sind nicht zu bremsen.\"",
        ) #possibly base data
        event1.save()
        event2 = Event(
            event_name="JOHNNY & ME",
            event_type=EventType.CINEMA,
            event_description="Eine Zeitreise mit Johnny Heartfield",
        )
        event2.save()
        event1day1 = EventDay(
            event_name=event1,
            date=parse_datetime("2024-02-24"),
            start_time=parse_datetime("2024-02-24 20:00:00").replace(tzinfo=get_current_timezone()),
            duration=parse_duration("0 5:00:00"),
            admission_time=parse_datetime("2024-02-24 19:30:00").replace(tzinfo=get_current_timezone()),
        )
        event1day1.save()
        event1day2 = EventDay(
            event_name=event1,
            date=parse_datetime("2024-03-08"),
            start_time=parse_datetime("2024-03-08 20:00:00").replace(tzinfo=get_current_timezone()),
            duration=parse_duration("0 5:00:00"),
            admission_time=parse_datetime("2024-03-08 19:30:00").replace(tzinfo=get_current_timezone()),
        )
        event1day2.save()
        event2day1 = EventDay(
            event_name=event2,
            date=parse_datetime("2024-02-12"),
            start_time=parse_datetime("2024-02-12 20:00:00").replace(tzinfo=get_current_timezone()),
            duration=parse_duration("0 2:17:00"),
            admission_time=parse_datetime("2024-02-12 19:50:00").replace(tzinfo=get_current_timezone()),
        )
        event2day1.save()
        act1 = Act(act_name="DJ Malhalla und DJ Petrike", person_count=2) #possibly base data
        act1.save()
        eventact1 = EventAct(
            event_day=EventDay.objects.get(start_time=parse_datetime("2024-02-24 20:00:00").replace(tzinfo=get_current_timezone())),
            act_name=act1,
        )
        eventact1.save()
        eventact2 = EventAct(
            event_day=EventDay.objects.get(start_time=parse_datetime("2024-03-08 20:00:00").replace(tzinfo=get_current_timezone())),
            act_name=act1,
        )
        eventact2.save()
