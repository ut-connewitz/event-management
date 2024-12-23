from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.utils.timezone import get_current_timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView

from backend.models.user import User, TeamMember, UTMember, UserAdress
from backend.models.task import Task, Urgency, State, Volunteering, DeletedVolunteering
from backend.models.misc import Adress

class ProfileHub(LoginRequiredMixin, TemplateView):
    template_name = 'profile_page/profile_hub.html'
    today = datetime.now(tz=get_current_timezone()).date()
    next_week = today + timedelta(hours=168)

    def get_user_volunteering(self, user):

        # the following evaluates to:
        # SELECT * from volunteering
        # WHERE (user = user AND task.event_day.date > today)
        # it returns a queryset not a list of objects
        user_volunteerings = Volunteering.objects.filter(user=user).filter(task__event__date__gte=self.today)

        return user_volunteerings

    def generate_task_links(self, user_volunteerings):
        user_task_html = ''

        for volunteering in user_volunteerings:
            user_task_html += f'<li>{volunteering.task.get_html_url} {volunteering.task.event}</li>'

        if user_task_html != '':
            return f"<td><ul> {user_task_html} </ul></td>"
        return '<td>Keine aktuellen Dienste</td>'

    def get_deleted_volunteerings(self):
        deleted_volunteerings = DeletedVolunteering.objects.filter(task__event__date__gte=self.today).filter(task__event__date__lte=self.next_week)
        return deleted_volunteerings

    def generate_deleted_volunteering_links(self, deleted_volunteerings):
        deleted_volunteerings_html = ''

        if not deleted_volunteerings:
            return '<td>Keine kurzfristig abgesagten Dienste</td>'
        else:
            for volunteering in deleted_volunteerings:
                deleted_volunteerings_html += f'<li>{volunteering.task.get_html_url} {volunteering.task.event}</li>'
            return f"<td><ul> {deleted_volunteerings_html} </ul></td>"

    def get_urgent_tasks(self):
        urgent_tasks = Task.objects.filter(event__date__gte=self.today).filter(event__date__lte=self.next_week).filter(urgency=Urgency.URGENT).filter(state=State.FREE)
        return urgent_tasks

    def generate_urgent_tasks_links(self, urgent_tasks):
        urgent_tasks_html = ''

        if not urgent_tasks:
            return '<td>Keine drigenden Aufgaben</td>'
        else:
            for task in urgent_tasks:
                urgent_tasks_html += f'<li>{task.get_html_url} {task.event}</li>'
            return f"<td><ul> {urgent_tasks_html} </ul></td>"

    def get_user_teams(self, user):
        user_teams = TeamMember.objects.filter(user=user)
        user_has_teams = False
        if user_teams:
            user_has_teams = True
        return user_has_teams, user_teams

    def generate_user_teams_html(self, user_teams):
        user_teams_html = ''

        if not user_teams:
            return user_teams_html
        else:
            for team_membership in user_teams:
                user_teams_html += f'<li>{team_membership.team.name} </li>'
            return f"<td><ul> {user_teams_html} </ul></td>"

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_pk = user.pk
        user_adress = None
        adress = None
        adress_pk = None

        try:
            user_adress = UserAdress.objects.get(pk=user_pk)
            adress = user_adress.adress
            adress_pk = adress.adress_id
        except UserAdress.DoesNotExist:
            pass

        user_volunteerings = self.get_user_volunteering(user)
        user_task_html = self.generate_task_links(user_volunteerings)
        deleted_volunteerings = self.get_deleted_volunteerings()
        deleted_volunteerings_html = self.generate_deleted_volunteering_links(deleted_volunteerings)
        urgent_tasks = self.get_urgent_tasks()
        urgent_tasks_html = self.generate_urgent_tasks_links(urgent_tasks)
        user_has_teams, user_teams = self.get_user_teams(user)
        user_teams_html = self.generate_user_teams_html(user_teams)
        context['user_task_html'] = mark_safe(user_task_html)
        context['deleted_volunteerings_html'] = mark_safe(deleted_volunteerings_html)
        context['urgent_tasks_html'] = mark_safe(urgent_tasks_html)
        context['user_has_teams'] = user_has_teams
        context['user_teams_html'] = mark_safe(user_teams_html)

        context['user_pk'] = user_pk
        context['user_adress'] = user_adress
        context['adress_pk'] = adress_pk

        return context

class Account(LoginRequiredMixin, UpdateView):
    model = User
    #if self.request.user.is_staff:
        #fields = '__all__'
    #else:
    fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    template_name ='profile_page/account.html'

    # first built in method that is called when the view is used
    # used here to check if the user instance given by the url belongs to the logged in user
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().pk != request.user.id:
            raise Http404('Falscher Account.') # PermissionDenied() from django.core.exceptions
        return super(Account, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.email:
            user_email = user.email
        else:
            user_email = None
        membership_number = None
        try:
            member = UTMember.objects.get(user=user)
        except UTMember.DoesNotExist:
            member = None

        if member != None:
            membership_number = member.member_number

        context['membership_number'] = membership_number
        context['user_email'] = user_email

        return context

class CreateAdress(LoginRequiredMixin, CreateView):
    model = Adress
    fields = ['street', 'house_number', 'postal_code', 'country']

    template_name ='profile_page/adress.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        user_adress = UserAdress.objects.create(
            user = form.instance.user,
            adress = self.object,
        )
        user_adress.save()
        return super().form_valid(form)


class UpdateAdress(LoginRequiredMixin, UpdateView):
    model = Adress
    fields = ['street', 'house_number', 'postal_code', 'country']

    template_name ='profile_page/adress.html'

    # first built in method that is called when the view is used
    # used here to check if the user instance given by the url belongs to the logged in user
    def dispatch(self, request, *args, **kwargs):
        req_user_adress = None
        req_adress_pk = None

        try:
            req_user_adress = UserAdress.objects.get(pk=request.user.id)
            req_adress = req_user_adress.adress
            req_adress_pk = req_adress.adress_id
        except UserAdress.DoesNotExist:
            pass

        if self.get_object().pk != req_adress_pk:
            raise Http404('Falscher Account.')
        return super(UpdateAdress, self).dispatch(request, *args, **kwargs)
