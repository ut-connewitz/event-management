from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.utils.timezone import get_current_timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView

from backend.models.user import User, UTMember, Adress
from backend.models.task import Volunteering, DeletedVolunteering
#from .forms import AccountForm

class ProfileHub(LoginRequiredMixin, TemplateView):
    template_name = 'profile_page/profile_hub.html'

    def get_user_volunteering(self, user):
        today = datetime.now(tz=get_current_timezone()).date()

        # the following evaluates to:
        # SELECT * from volunteering
        # WHERE (user = user AND task.event_day.date > today)
        # it returns a queryset not a list of objects
        user_volunteerings = Volunteering.objects.filter(user=user).filter(task__event_day__date__gte=today)

        return user_volunteerings

    def generate_task_links(self, user_volunteerings):
        user_task_html = ''

        for volunteering in user_volunteerings:
            user_task_html += f'<li>{volunteering.task.get_html_url} {volunteering.task.event_day}</li>'

        if user_task_html != '':
            return f"<td><ul> {user_task_html} </ul></td>"
        return '<td>Keine aktuellen Dienste</td>'

    def get_deleted_volunteerings(self):
        today = datetime.now(tz=get_current_timezone()).date()
        next_week = today + timedelta(hours=168)
        deleted_volunteerings = DeletedVolunteering.objects.filter(task__event_day__date__gte=today).filter(task__event_day__date__lte=next_week)
        return deleted_volunteerings

    def generate_deleted_volunteering_links(self, deleted_volunteerings):
        deleted_volunteerings_html = ''

        if not deleted_volunteerings:
            return '<td>Keine kurzfristig abgesagten Dienste</td>'
        else:
            for volunteering in deleted_volunteerings:
                deleted_volunteerings_html += f'<li>{volunteering.task.get_html_url} {volunteering.task.event_day}</li>'
            return f"<td><ul> {deleted_volunteerings_html} </ul></td>"


    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_pk = user.pk
        adress = None

        try:
            adress = Adress.objects.get(pk=user_pk)
        except Adress.DoesNotExist:
            pass

        user_volunteerings = self.get_user_volunteering(user)
        user_task_html = self.generate_task_links(user_volunteerings)
        deleted_volunteerings = self.get_deleted_volunteerings()
        deleted_volunteerings_html = self.generate_deleted_volunteering_links(deleted_volunteerings)
        context['user_task_html'] = mark_safe(user_task_html)
        context['deletd_volunteerings_html'] = mark_safe(deleted_volunteerings_html)

        context['user_pk'] = user_pk
        context['adress'] = adress

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
            raise Http404('Falscher Account.')
        return super(Account, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        membership_number = None
        try:
            member = UTMember.objects.get(user=user)
        except UTMember.DoesNotExist:
            member = None

        if member != None:
            membership_number = member.member_number

        context['membership_number'] = membership_number

        return context

class CreateAdress(LoginRequiredMixin, CreateView):
    model = Adress
    fields = ['street', 'house_number', 'postal_code', 'country']

    template_name ='profile_page/adress.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateAdress(LoginRequiredMixin, UpdateView):
    model = Adress
    fields = ['street', 'house_number', 'postal_code', 'country']

    template_name ='profile_page/adress.html'

    # first built in method that is called when the view is used
    # used here to check if the user instance given by the url belongs to the logged in user
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().pk != request.user.id:
            raise Http404('Falscher Account.')
        return super(UpdateAdress, self).dispatch(request, *args, **kwargs)
