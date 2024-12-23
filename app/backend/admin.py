from typing import Set

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import (GroupAdmin, UserAdmin)
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm
from django.core.exceptions import ValidationError

from backend.forms import CustomUserCreationForm, CustomUserChangeForm, CustomAdminPasswordChangeForm
from backend.models.setting import (Setting, UserSettingValue, BoolValue, IntValue, EnumValue)
from backend.models.user import (AdminGroup, AdminGroupMember, User, UTMember, UserAdress, Team, TeamMember)
from backend.models.event import(Event, EventSeries, Act, EventAct, PastEvent, Location)
from backend.models.notification import (NotificationType, Notification, TaskNotification, VolunteeringNotification)
from backend.models.task import (TaskType, TeamRestriction, Urgency, State, Task, ConfirmationType, Volunteering, DeletedVolunteering)
from backend.models.misc import Adress

# some admin site customisation
# link to website
admin.site.site_url = "/ecal/calendar"
admin.site.site_header = "UT Connewitz Veranstaltungen"
admin.site.site_title = "UT Connewitz Veranstaltungen"
admin.site.index_title = "Administration"



# inlines
class AdminGroupMemberInline(admin.TabularInline):
    model = AdminGroupMember
    extra = 1
    classes = ('collapse')

class EventInline(admin.StackedInline):
    model = Event
    extra = 0

class EventActInline(admin.TabularInline):
    model = EventAct
    extra = 1
    classes = ('collapse')

class LocationInline(admin.StackedInline):
    model = Location
    extra = 0
    classes = ('collapse')

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1

class UTMemberInline(admin.TabularInline):
    model = UTMember
    extra = 0
    classes = ('collapse')

class UserAdressInline(admin.StackedInline):
    model = UserAdress
    extra = 0
    classes = ('collapse')

class UserGroupInline(admin.TabularInline):
    model = User.groups.through
    raw_id_fields=("user",)
    extra = 1
    classes = ('collapse')

class VolunteeringInline(admin.TabularInline):
    model = Volunteering
    extra = 0
    classes = ('collapse')


# admins
class AdressAdmin(admin.ModelAdmin):
    model = Adress
    inlines = [
        UserAdressInline,
        LocationInline,
    ]

class AdminGroupAdmin(GroupAdmin):
    inlines = [
        UserGroupInline,
    ]

class AdminGroupMemberAdmin(admin.ModelAdmin):
    model = AdminGroupMember
    ordering = ["user"]
    list_display = ["user", "admin_group"]
    list_filter = ["user", "admin_group"]

class TeamAdmin(admin.ModelAdmin):
    model = Team

class TeamMemberAdmin(admin.ModelAdmin):
    model = TeamMember
    ordering = ["user"]
    list_display = ["user", "team"]
    list_filter = ["user", "team"]

class EventAdmin(admin.ModelAdmin):
    model = Event
    inlines = [
        TaskInline,
        EventActInline,
    ]
    ordering = ["date"]
    list_display = ["series", "subtitle", "date", "start_time", "location"]
    list_filter = ["series", "subtitle", "date", "location"]

class PastEventAdmin(admin.ModelAdmin):
    model = PastEvent
    ordering = ["date"]
    list_display = ["series", "subtitle", "date", "start_time", "location"]
    list_filter = ["series", "subtitle", "date", "location"]
    readonly_fields = [
        'series',
        'subtitle',
        'date',
        'start_time',
        'duration',
        'location',
    ]

class EventSeriesAdmin(admin.ModelAdmin):
    inlines = [
        EventInline,
    ]
    ordering = ["event_name"]
    list_display = ["event_name", "event_type"]
    list_filter = ["event_name", "event_type"]

class TaskAdmin(admin.ModelAdmin):
    model = Task
    inlines = [
        VolunteeringInline,
    ]
    ordering = ["event"]
    list_display = ["event", "task_type", "team_restriction", "urgency", "state"]
    list_filter = ["event", "task_type", "team_restriction", "urgency", "state"]

# unregister the provided admin
#admin.site.unregister(User)

#register own model admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # assign the custom forms to the add_form (user creation) and form (user editing) variables
    # these variables should be automatically used by django
    # since the get_form() method of this class is overwritten (see further below)
    # the specific form is used depending on an user object is already exisiting or not
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    change_password_form = CustomAdminPasswordChangeForm

    model = User
    # defining how users are represented in the user list in the admin panel
    list_display = ["username", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "groups"]
    # defining the fields shown when editing a user
    fieldsets = [
        (None,
            {
                "fields": [
                    "username",
                    "password",
                    ],
            },
        ),
        ("Person",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    ],
            },
        ),
        ("Kontakt",
            {
                "fields": [
                    "email",
                    "phone",
                    ],
            },
        ),
        ("Berechtigungen",
            {
                "fields": [
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "user_permissions",
                    ],
            },
        ),
        ("Aktivität",
            {
                "fields": [
                    "date_joined",
                    "last_login",
                    ],
            },
        ),
    ]
    # defining the fields when creating a user
    add_fieldsets = [
        (None,
            {
                "classes": [
                    "wide",
                    ],
                "fields": [
                    "username",
                    "email",
                    "password1",
                    "password2",
                    ],
            },
        ),
    ]

    search_fields = ["username"]
    ordering = ["username"]
    filter_horizontal = []

    readonly_fields = [
        'date_joined',
        'last_login',
    ]

    actions = [
        'activate_users',
    ]

    inlines = [
        AdminGroupMemberInline,
        TeamMemberInline,
        UTMemberInline,
        UserAdressInline,
    ]

    # this modifies the form for creating/editing users depending on the
    # logged in accounts status / permissions
    def get_form(self, request, obj=None, **kwargs):
        # here it is explicitly set, which form to use depending on if a user object is given or not
        if obj is None:
            kwargs["form"] = CustomUserCreationForm
        else:
            kwargs["form"] = CustomUserChangeForm

        form = super().get_form(request, obj, **kwargs)

        is_superuser = request.user.is_superuser
        disabled_fields = set()
        # prevent permission escalation
        # not superusers should not be able to edit admin and superuser status
        # or the username of other users
        if not is_superuser:
            disabled_fields |= {
                'is_staff',
                'username',
                'is_superuser',
                'user_permissions',
            }
        # not superusers should not be able to edit their own permissions
        # but they should be able to edit the username during account creation
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
        # additional protection for superuser accounts
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
        # when a new user object is created, the username should be editable
        if obj is None:
            disabled_fields -= {
                'username',
            }

        if obj == request.user:
            disabled_fields -= {
                'username',
            }

        for field in disabled_fields:
            if field in form.base_fields:
                form.base_fields[field].disabled = True

        #kwargs["form"] = form
        #return super().get_form(request, obj, **kwargs)
        return form

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
#admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAdress)
admin.site.register(UTMember)
admin.site.register(Adress, AdressAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(AdminGroup, AdminGroupAdmin)
admin.site.register(AdminGroupMember, AdminGroupMemberAdmin)
#admin.site.register(EventType)
admin.site.register(EventSeries, EventSeriesAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Act)
admin.site.register(EventAct)
admin.site.register(PastEvent, PastEventAdmin)
admin.site.register(Location)
#admin.site.register(TaskType)
#admin.site.register(TeamRestriction)
#admin.site.register(Urgency)
#admin.site.register(State)
#admin.site.register(ConfirmationType)
admin.site.register(Task, TaskAdmin)
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
