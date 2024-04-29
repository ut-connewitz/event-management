from datetime import datetime, timedelta, date
import calendar

from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from backend.models.event import EventDay
from backend.models.task import Task
from .utils import Calendar
from .forms import EventDayForm, TaskForm


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = EventDay
    template_name = 'events_calendar/calendar.html'

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event_day(request, event_day_id=None):
    instance = EventDay()
    if event_day_id:
        instance = get_object_or_404(EventDay, pk=event_day_id)
    else:
        instance = EventDay()

    form = EventDayForm(request.POST or None, instance=instance)
    if not request.user.is_staff:
        form.fields['event'].disabled = True
        form.fields['date'].disabled = True
        form.fields['start_time'].disabled = True
        form.fields['duration'].disabled = True
        form.fields['admission_time'].disabled = True

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('events_calendar:calendar'))
    return render(request, 'events_calendar/event_day.html', {'form':form})

@login_required
def task(request, task_id=None):
    instance = Task()
    if task_id:
        instance = get_object_or_404(Task, pk=task_id)
    else:
        instance = Task()

    form = TaskForm(request.POST or None, instance=instance)
    if not request.user.is_staff:
        form.fields['event_day'].disabled = True
        form.fields['task_type'].disabled = True
        form.fields['team_restriction'].disabled = True
        form.fields['urgency'].disabled = True
        form.fields['state'].disabled = True
        form.fields['start_time'].disabled = True
        form.fields['finish_time'].disabled = True
        form.fields['comment'].disabled = True
        # this loop did not work: File "/app/events_calendar/views.py", line 90, in task 'field.disabled = True'
        #for field in form.fields:
        #    field.disabled = True

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('events_calendar:calendar'))
    return render(request, 'events_calendar/task.html', {'form':form})

def index(request):
    return HttpResponse('hello')
