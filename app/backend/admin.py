from typing import Set

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import (GroupAdmin, UserAdmin)

from backend.models.setting import (Setting, UserSettingValue, BoolValue, IntValue, EnumValue)
from backend.models.user import (User, UTMember, Adress, Team, TeamMember)
from backend.models.event import(Event, EventSeries, Act, EventAct)
from backend.models.notification import (NotificationType, Notification, TaskNotification, VolunteeringNotification)
from backend.models.task import (TaskType, TeamRestriction, Urgency, State, Task, ConfirmationType, Volunteering, DeletedVolunteering)

# some admin site customisation
# link to website
admin.site.site_url = "/ecal/calendar"
admin.site.site_header = "UT Connewitz Veranstaltungen"
admin.site.site_title = "UT Connewitz Veranstaltungen"
admin.site.index_title = "Administration"



class UTMemberInLine(admin.TabularInline):
    model = UTMember

class UserAdressInLine(admin.TabularInline):
    model = Adress

class TeamMemberInLine(admin.TabularInline):
    model = TeamMember

class UserAdmin(admin.ModelAdmin):
    inlines = [
        TeamMemberInLine,
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

class EventInLine(admin.TabularInline):
    model = Event

class EventSeriesAdmin(admin.ModelAdmin):
    inlines = [
        EventInLine,
    ]

class TaskInline(admin.TabularInline):
    model = Task

class EventAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline
    ]

# unregister the provided admin
#admin.site.unregister(User)

#register own model admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        # prevent permission escalation
        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions',
            }

        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff', # maybe move this the list above
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True

        return form


    readonly_fields = [
        'date_joined',
    ]

    actions = [
        'activate_users',
    ]

    def activate_users(self, request, queryset):
        assert request.user.has_perm('backend.change_user')
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, '{} Accounts aktiviert.'.format(cnt))
    activate_users.short_description = "Accounts aktivieren"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm('backend.change_user'):
            del actions['activate_users']
        return actions


# Register your models here.
admin.site.unregister(Group)
#admin.site.register(User, UserAdmin)
admin.site.register(UTMember)
admin.site.register(Adress)
admin.site.register(Team, MyGroupAdmin)
admin.site.register(TeamMember)
#admin.site.register(EventType)
admin.site.register(EventSeries, EventSeriesAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Act)
admin.site.register(EventAct)
#admin.site.register(TaskType)
#admin.site.register(TeamRestriction)
#admin.site.register(Urgency)
#admin.site.register(State)
#admin.site.register(ConfirmationType)
admin.site.register(Task)
admin.site.register(Volunteering)
admin.site.register(DeletedVolunteering) #debug, unregister later
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
