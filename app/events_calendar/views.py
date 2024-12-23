from datetime import datetime, timedelta, date
import calendar
import logging

from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import HiddenInput


from backend.models.event import Event, PastEvent
from backend.models.task import Task, Volunteering, ConfirmationType, State
from .utils import Calendar
from .forms import EventForm, PastEventForm, TaskForm, VolunteeringForm


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Event
    template_name = 'events_calendar/calendar.html'

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        today = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        calendar = Calendar(self.request.user, today.year, today.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_calendar = calendar.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_calendar)

        context['prev_month'] = prev_month(today)
        context['next_month'] = next_month(today)
        return context

def get_date(requested_day):
    if requested_day:
        year, month = (int(x) for x in requested_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(today):
    first = today.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(today):
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    last = today.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
        initial_date = instance.date.strftime('%d.%m.%Y')
    else:
        instance = Event()
        event_id = instance.event_id
        initial_date = now().date().strftime('%d.%m.%Y')
        #logger = logging.getLogger(__name__) #debug
        #logger.error('new instance id: '+str(event_day_id)) #debug

    #logger = logging.getLogger(__name__) #debug
    #logger.error(str(instance.date)) #debug
    #logger.error(str(instance.date.strftime('%d.%m.%Y')))

    form = EventForm(
        request.POST or None,
        instance=instance,
        initial={
            'date': initial_date
        }
    )
    if not request.user.is_staff:
        form.fields['series'].disabled = True
        form.fields['subtitle'].disabled = True
        form.fields['date'].disabled = True
        form.fields['start_time'].disabled = True
        form.fields['duration'].disabled = True
        form.fields['admission_time'].disabled = True
        form.fields['location'].disabled = True

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ecal:calendar'))

    context = {
        'event_id' : event_id,
        'form': form,
    }
    return render(request, 'events_calendar/event.html', context=context)

@login_required
def past_event(request, past_event_id=None):

    instance = get_object_or_404(PastEvent, pk=past_event_id)

    form = PastEventForm(
        request.POST or None,
        instance=instance,
        initial={
            'date': instance.date.strftime('%d.%m.%Y')
        }
    )

    form.fields['series'].disabled = True
    form.fields['subtitle'].disabled = True
    form.fields['date'].disabled = True
    form.fields['start_time'].disabled = True
    form.fields['duration'].disabled = True
    form.fields['location'].disabled = True

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('ecal:calendar'))

    context = {
        'past_event_id' : past_event_id,
        'form': form,
    }
    return render(request, 'events_calendar/past_event.html', context=context)

@login_required
def task(request, task_id=None, volunteering_id=None, event_id=None):
    task_instance = Task()
    if task_id:
        task_instance = get_object_or_404(Task, pk=task_id)
    else:
        task_instance = Task()

    task_id = task_instance.task_id

    volunteering_instance = Volunteering()
    is_new_volunteering = False
    try:
        volunteering_instance = Volunteering.objects.get(
            task = task_instance,
        )
    except Volunteering.DoesNotExist:
        volunteering_instance = Volunteering(
            task = task_instance,
            user = request.user,
        )
        is_new_volunteering = True


    if event_id:
        event = Event.objects.get(event_id=event_id)
        task_form = TaskForm(request.POST or None, instance=task_instance, initial={'event': event})
    else:
        task_form = TaskForm(request.POST or None, instance=task_instance)

    volunteering_form = VolunteeringForm(
        request.POST or None,
        instance=volunteering_instance,
        initial={
            'confirmation_type': ConfirmationType.YES,
            'user': request.user,
        })
    if is_new_volunteering:
        volunteering_form.fields['confirmation_type'].disabled = True

    if not request.user.is_staff:
        task_form.fields['event'].disabled = True
        task_form.fields['task_type'].disabled = True
        task_form.fields['team_restriction'].disabled = True
        task_form.fields['urgency'].disabled = True
        #task_form.fields['state'].disabled = True # set to 'editable=False' in model, so it doesnt exist as field here
        task_form.fields['start_time'].disabled = True
        task_form.fields['finish_time'].disabled = True
        task_form.fields['comment'].disabled = True

        volunteering_form.fields['user'].widget = HiddenInput()
        volunteering_form.fields['task'].widget = HiddenInput()
        #volunteering_form.fields['user'].widget.attrs['readonly'] = True
        #volunteering_form.fields['task'].widget.attrs['readonly'] = True
        if request.user != volunteering_instance.user:
            volunteering_form.fields['confirmation_type'].widget = HiddenInput()
            volunteering_form.fields['comment'].widget = HiddenInput()
            #volunteering_form.fields['confirmation_type'].widget.attrs['readonly'] = True
            #volunteering_form.fields['confirmation_type'].disabled

        #    volunteering_form.fields['user'].widget = HiddenInput()

        # experimental integration of ConfirmationType.MAYBE
        # idea: show volunteering, but do not show, who cofirmed with maybe
        # make it possible, to confirm with ConfirmationType.YES only and delete previous MAYBE confirmation
        # problem: when save button is clicked without changing anything an error is thrown, that makes ALL form fields freely accesible
        # so the user could select anyone for any task
        #elif request.user != volunteering_instance.user and volunteering_instance.confirmation_type == ConfirmationType.MAYBE:
        #    volunteering_form.fields['user'].widget = HiddenInput()

        # this loop did not work: File "/app/events_calendar/views.py", line 90, in task 'field.disabled = True'
        #for field in form.fields:
        #    field.disabled = True

    if request.method == 'POST':
        if 'edit_task' in request.POST:
            if task_form.is_valid():
                task_form.save()
                return HttpResponseRedirect(reverse('ecal:calendar'))

        if 'edit_volunteering' in request.POST and (request.user == volunteering_instance.user or request.user.is_staff):
            if volunteering_form.is_valid() and request.POST.get('volunteering_button')=="volunteering":
                confirmation_type = volunteering_form.cleaned_data["confirmation_type"]
                volunteering_form.save()
                # volunteering state change logic located at model file (backend/models/task/volunteering.py)
                # in order to make it effective regardless of the source of the change

                return HttpResponseRedirect(reverse('ecal:calendar'))

    # note: context variables are accessable within template code blocks
    # e.g. {% if request.user == volunteering_instance.user %}
    context = {
        'task_form': task_form,
        'volunteering_form': volunteering_form,
        'volunteering_instance': volunteering_instance,
    }
    return render(request, 'events_calendar/task.html', context=context)
