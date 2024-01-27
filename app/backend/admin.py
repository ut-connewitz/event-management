from django.contrib import admin


from backend.models import (
User, UTMember, Volunteer, Adress, Team, TeamMember,
Event, EventDay, Act, EventAct,
Task, Volunteering,
Notification, TaskNotification, VolunteeringNotification,
Setting, UserSettingValue, BoolValue, IntValue, EnumValue
)


# Register your models here.
admin.site.register(User)
admin.site.register(UTMember)
admin.site.register(Volunteer)
admin.site.register(Adress)
admin.site.register(Team)
admin.site.register(TeamMember)
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
