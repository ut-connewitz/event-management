from django.contrib import admin

from backend.models.setting import (Setting, UserSettingValue, BoolValue, IntValue, EnumValue)
from backend.models.user import (User, UTMember, Volunteer, Adress)
from backend.models.event import(Event, EventDay, Act, EventAct)
from backend.models.notification import (NotificationType, Notification, TaskNotification, VolunteeringNotification)
from backend.models.task import (TaskType, TeamRestriction, Urgency, State, Task, ConfirmationType, Volunteering)

class UTMemberInLine(admin.TabularInline):
    model = UTMember

class UserAdmin(admin.ModelAdmin):
    inlines = [
        UTMemberInLine
    ]

class VolunteerInLine(admin.TabularInline):
    model = Volunteer

class UserAdmin(admin.ModelAdmin):
    inlines = [
        VolunteerInLine,
    ]

# Register your models here.
admin.site.register(User)
admin.site.register(UTMember)
admin.site.register(Volunteer)
admin.site.register(Adress)
#admin.site.register(Team) #deprecated
#admin.site.register(TeamMember)#deprecated
#admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(EventDay)
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
admin.site.register(Notification)
admin.site.register(TaskNotification)
admin.site.register(VolunteeringNotification)
#admin.site.register(SettingType)
#admin.site.register(ValueType)
admin.site.register(Setting)
admin.site.register(UserSettingValue)
admin.site.register(BoolValue)
admin.site.register(IntValue)
admin.site.register(EnumValue)
