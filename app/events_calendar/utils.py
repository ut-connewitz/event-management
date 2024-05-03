from datetime import datetime, timedelta
from calendar import HTMLCalendar
from backend.models.event import EventDay
from backend.models.task import Task, State


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    #formats a days as td
    #filters event_days by day
    def formatday(self, day, event_days):
        events_per_day = event_days.filter(start_time__day=day)
        day_content = ''

        for event_day in events_per_day:
            day_content += f'<li>{event_day.get_html_url} </li>'
            tasks = Task.objects.filter(event_day=event_day, state=State.FREE)
            task_html = ''

            for task in tasks:
                task_html += f'<li>{task.get_html_url} </li>'

            if task_html != '':
                day_content += f'<ul>' + task_html +f'</ul>'

        if day!= 0:
            return f"<td><span class='date'>{day}</span><ul> {day_content} </ul></td>"
        return '<td></td>'

    #formats a week as tr
    def formatweek(self, theweek, event_days):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, event_days)
        return f'<tr> {week} </tr>'

    #formats a month as a table
    #filters event_days by year and month
    def formatmonth(self, withyear=True):
        event_days = EventDay.objects.filter(start_time__year=self.year, start_time__month=self.month)
        #cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal = f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
		          cal += f'{self.formatweek(week, event_days)}\n'
        cal += f'</table>'
        return cal
