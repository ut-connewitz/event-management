from datetime import datetime, timedelta
from calendar import HTMLCalendar
from backend.models.event import EventDay


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    #formats a days as td
    #filters event_days by day
    def formatday(self, day, event_days):
        events_per_day = event_days.filter(start_time__day=day)
        d = ''
        for event_day in events_per_day:
            d += f'<li>{event_day.event.event_name} </li>'

        if day!= 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
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
