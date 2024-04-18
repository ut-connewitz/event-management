from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

from backend.models.setting import (Setting, UserSettingValue, BoolValue, IntValue, EnumValue)
from backend.models.user import (User, UTMember, Adress, Team, TeamMember)
from backend.models.event import(Event, EventDay, Act, EventAct)
from backend.models.notification import (NotificationType, Notification, TaskNotification, VolunteeringNotification)
from backend.models.task import (TaskType, TeamRestriction, Urgency, State, Task, ConfirmationType, Volunteering)

class UTMemberInLine(admin.TabularInline):
    model = UTMember

#class VolunteerInLine(admin.TabularInline):
#    model = Volunteer

class UserAdressInLine(admin.TabularInline):
    model = Adress

class UserAdmin(admin.ModelAdmin):
    inlines = [
        #VolunteerInLine,
        UTMemberInLine,
        UserAdressInLine,
    ]

class UserGroupInLine(admin.TabularInline):
    model = User.groups.through
    raw_id_fields=("user",)

class MyGroupAdmin(GroupAdmin):
    inlines = [
        UserGroupInLine,
    ]

class EventDayInLine(admin.TabularInline):
    model = EventDay

class EventAdmin(admin.ModelAdmin):
    inlines = [
        EventDayInLine,
    ]

class TaskInline(admin.TabularInline):
    model = Task

class EventDayAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline
    ]

# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(UTMember)
#admin.site.register(Volunteer) #deprecated
admin.site.register(Adress)
admin.site.register(Team, MyGroupAdmin)
admin.site.register(TeamMember)
#admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
admin.site.register(EventDay, EventDayAdmin)
admin.site.register(Act)
admin.site.register(EventAct)
#admin.site.register(TaskType)
#admin.site.register(TeamRestriction)
#admin.site.register(Urgency)
#admin.site.register(State)
#admin.site.register(ConfirmationType)
admin.site.register(Task)
admin.site.register(Volunteering)
#admin.site.register(NotificationType)
#admin.site.register(Notification)
#admin.site.register(TaskNotification)
#admin.site.register(VolunteeringNotification)
#admin.site.register(SettingType)
#admin.site.register(ValueType)
#admin.site.register(Setting)
#admin.site.register(UserSettingValue)
#admin.site.register(BoolValue)
#admin.site.register(IntValue)
#admin.site.register(EnumValue)
