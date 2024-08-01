from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime, parse_time
from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import Group, Permission

from backend.models.setting import (Setting, UserSettingValue, BoolValue, IntValue, EnumValue)
from backend.models.user import (AdminGroup, AdminGroupMember, User, UTMember, Adress, Team, TeamMember)
from backend.models.event import(EventType, EventSeries, Event, Act, EventAct)
from backend.models.notification import (NotificationType, Notification, TaskNotification, VolunteeringNotification)
from backend.models.task import (TaskType, TeamRestriction, Urgency, State, Task, ConfirmationType, Volunteering)

class Command(BaseCommand):
    help = "Fügt der Datenbank Testdaten hinzu"

    def handle(self, *args, **options):
        self.stdout.write("running command addtestdata")
        today = datetime.now(tz=get_current_timezone()).date()
        # some different dates for testing purposes
        date_within_next_week = today + timedelta(hours=100)
        date_within_the_week_after = today + timedelta(hours=200)
        date_in_the_past = today - timedelta(hours=100)

        user1 = User.objects.create(
            username="jd",
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@mail.de",
        )
        user1.set_password('lazy1234')
        user1.save()

        utmember1 = UTMember(
            user = User.objects.get(username="jd"),
            member_number = 1
        )
        utmember1.save()


        user2 = User.objects.create(
            username="mm",
            first_name="Max",
            last_name="Mustermann",
            email="max@mustermail.net",
        )
        user2.set_password("lazy1234")
        user2.save()

        adress_jd = Adress(
            user=User.objects.get(username="jd"),
            street="Forstweg",
            house_number="13a",
            postal_code="43221",
        )
        adress_jd.save()



        #base and testdata for event
        # add some event series
        event_series1 = EventSeries(
            event_name="BAIKALTRAIN DISCO",
            event_type=EventType.EXTRA,
            event_description="Disko mit DJ Malhalla und DJ Petrike",
            event_press="Knackige Tanzmusik vom Balkan bis zum Baikal. \"Von der Eisenbahn in den Club. Die Leute sind nicht zu bremsen.\"",
        ) #possibly base data
        event_series1.save()

        event_series2 = EventSeries(
            event_name="JOHNNY & ME",
            event_type=EventType.CINEMA,
            event_description="Eine Zeitreise mit Johnny Heartfield",
        )
        event_series2.save()

        #add some event days
        event1 = Event(
            series=EventSeries.objects.get(event_name="BAIKALTRAIN DISCO"),
            date=parse_datetime("2024-02-24"),
            start_time=parse_time("20:00:00").replace(tzinfo=get_current_timezone()),
            duration=300,
            admission_time=parse_time("19:30:00").replace(tzinfo=get_current_timezone()),
        )
        event1.save()

        event2 = Event(
            series=EventSeries.objects.get(event_name="BAIKALTRAIN DISCO"),
            date=parse_datetime("2024-03-08"),
            start_time=parse_time("20:00:00").replace(tzinfo=get_current_timezone()),
            duration=300,
            admission_time=parse_time("19:30:00").replace(tzinfo=get_current_timezone()),
        )
        event2.save()

        event3 = Event(
            series=EventSeries.objects.get(event_name="BAIKALTRAIN DISCO"),
            date=date_within_the_week_after,
            start_time=parse_time("20:00:00").replace(tzinfo=get_current_timezone()),
            duration=300,
            admission_time=parse_time("19:30:00").replace(tzinfo=get_current_timezone()),
        )
        event3.save()

        event4 = Event(
            series=EventSeries.objects.get(event_name="JOHNNY & ME"),
            date=parse_datetime("2024-02-12"),
            start_time=parse_time("20:00:00").replace(tzinfo=get_current_timezone()),
            duration=137,
            admission_time=parse_time("19:50:00").replace(tzinfo=get_current_timezone()),
        )
        event4.save()

        event5 = Event(
            series=EventSeries.objects.get(event_name="JOHNNY & ME"),
            date=date_within_next_week,
            start_time=parse_time("20:00:00").replace(tzinfo=get_current_timezone()),
            duration=137,
            admission_time=parse_time("19:50:00").replace(tzinfo=get_current_timezone()),
        )
        event5.save()

        event6 = Event(
            series=EventSeries.objects.get(event_name="JOHNNY & ME"),
            date=date_in_the_past,
            start_time=parse_time("20:00:00").replace(tzinfo=get_current_timezone()),
            duration=137,
            admission_time=parse_time("19:50:00").replace(tzinfo=get_current_timezone()),
        )
        event6.save()

        #add some tasks
        task1 = Task(
            event=Event.objects.get(date=date_within_the_week_after),
            task_type = TaskType.ADMISSION,
            urgency = Urgency.IMPORTANT,
        )
        task1.save()

        task2 = Task(
            event=Event.objects.get(date=date_within_the_week_after),
            task_type = TaskType.BAR,
            urgency = Urgency.MEDIUM,
        )
        task2.save()

        task3 = Task(
            event=Event.objects.get(date=date_within_the_week_after),
            task_type = TaskType.SOUND,
            team_restriction = TeamRestriction.SOUND,
            urgency = Urgency.IMPORTANT,
        )
        task3.save()

        task4 = Task(
            event=Event.objects.get(date=parse_datetime("2024-02-24")),
            task_type = TaskType.BAR,
            urgency = Urgency.MEDIUM,
        )
        task4.save()

        task5 = Task(
            event=Event.objects.get(date=parse_datetime("2024-02-24")),
            task_type = TaskType.ADMISSION,
            urgency = Urgency.URGENT,
        )
        task5.save()

        task6 = Task(
            event=Event.objects.get(date=date_within_next_week),
            task_type = TaskType.ADMISSION,
            urgency = Urgency.URGENT,
        )
        task6.save()

        task7 = Task(
            event=Event.objects.get(date=date_within_next_week),
            task_type = TaskType.BAR,
            urgency = Urgency.MEDIUM,
        )
        task7.save()

        task8 = Task(
            event=Event.objects.get(date=date_in_the_past),
            task_type = TaskType.ADMISSION,
            urgency = Urgency.URGENT,
        )
        task8.save()

        task9 = Task(
            event=Event.objects.get(date=date_in_the_past),
            task_type = TaskType.BAR,
            urgency = Urgency.MEDIUM,
        )
        task9.save()

        task10 = Task(
            event=Event.objects.get(date=date_within_next_week),
            task_type = TaskType.SOUND,
            team_restriction = TeamRestriction.SOUND,
            urgency = Urgency.IMPORTANT,
        )
        task10.save()

        task11 = Task(
            event=Event.objects.get(date=date_within_the_week_after),
            task_type = TaskType.LIGHT,
            team_restriction = TeamRestriction.LIGHT,
            urgency = Urgency.IMPORTANT,
        )
        task11.save()

        act1 = Act(act_name="DJ Malhalla und DJ Petrike", person_count=2) #possibly base data
        act1.save()

        eventact1 = EventAct(
            event=Event.objects.get(date=parse_datetime("2024-02-24").replace(tzinfo=get_current_timezone())),
            act=Act.objects.get(act_name="DJ Malhalla und DJ Petrike"),
        )
        eventact1.save()
        eventact2 = EventAct(
            event=Event.objects.get(date=parse_datetime("2024-03-08").replace(tzinfo=get_current_timezone())),
            act=Act.objects.get(act_name="DJ Malhalla und DJ Petrike"),
        )
        eventact2.save()
