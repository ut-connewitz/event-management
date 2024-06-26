from typing import Set

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import (GroupAdmin, UserAdmin)
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from backend.forms import CustomUserCreationForm, CustomUserChangeForm
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

#class UserAdmin(admin.ModelAdmin):
#    inlines = [
#        TeamMemberInLine,
#        UTMemberInLine,
#        UserAdressInLine,
#    ]

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
#@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = User
    list_display = ["username", "is_staff"]
    list_filter = ["is_staff"]
    fieldsets = [
        (None, {"fields": ["username", "password"]}),
        ("Person", {"fields": ["first_name", "last_name"]}),
        ("Berechtigungen", {"fields": ["is_superuser", "is_staff", "is_active", "user_permissions"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "fields": ["username", "email", "password1", "password2", "is_staff", "is_active", "user_permissions"],
            },
        ),
    ]

    search_fields = ["username"]
    ordering = ["username"]
    filter_horizontal = []


    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = CustomUserCreationForm
        else:
            kwargs["form"] = CustomUserChangeForm

        form = super().get_form(request, obj, **kwargs)

        is_superuser = request.user.is_superuser
        disabled_fields = set()
        # prevent permission escalation
        if not is_superuser:
            disabled_fields |= {
                'is_staff',
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
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        if (
            not is_superuser
            and obj is not None
            and obj.is_superuser == True
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'is_active',
                'password',
                'last_login',
                'date_joined',
                'username',
                'first_name',
                'last_name',
                'phone',
                'email',
            }

        if obj is None: # when a new user object is created, the username should be editable
            disabled_fields -= {
                'username',
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True

        #kwargs["form"] = form
        #return super().get_form(request, obj, **kwargs)
        return form


    readonly_fields = [
        'date_joined',
        'last_login',
    ]

    actions = [
        'activate_users',
    ]

    inlines = [
        TeamMemberInLine,
        UTMemberInLine,
        UserAdressInLine,
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
admin.site.register(User, CustomUserAdmin)
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
