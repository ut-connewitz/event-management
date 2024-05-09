from datetime import datetime, timedelta
from calendar import HTMLCalendar
from backend.models.event import EventDay
from backend.models.task import Task, State, Volunteering, TeamRestriction, Urgency
from backend.models.user import TeamMember


class Calendar(HTMLCalendar):
    def __init__(self,  user, year=None, month=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    def check_team_restriction(self, team_restriction, user_teams):
        for user_team in user_teams:
            if team_restriction == TeamRestriction.NONE:
                return True
            elif team_restriction == TeamRestriction.LIGHT:
                if user_team.team.name == "lichttechnik":
                    return True
            elif team_restriction == TeamRestriction.SOUND:
                if user_team.team.name == "tontechnik":
                    return True
            elif team_restriction == TeamRestriction.OFFICE:
                if user_team.team.name == "verwaltung":
                    return True

    #formats a days as td
    #filters event_days by day
    def formatday(self, day, event_days):
        events_per_day = event_days.filter(start_time__day=day)
        day_content = ''

        for event_day in events_per_day:
            day_content += f'<li>{event_day.get_html_url} </li>'
            free_tasks = Task.objects.filter(event_day=event_day, state=State.FREE)
            taken_tasks = Task.objects.filter(event_day=event_day, state=State.TAKEN)
            task_html = ''
            user_teams = TeamMember.objects.filter(user=self.user)


            for task in free_tasks:
                team_restriction = task.team_restriction
                pass_team_restriction = self.check_team_restriction(team_restriction, user_teams)
                if self.user.is_staff or pass_team_restriction:
                    if task.urgency == Urgency.URGENT:
                        task_html += f'<li class ="urgency_urgent">{task.get_html_url} (dringend!)</li>'
                    elif task.urgency == Urgency.IMPORTANT:
                        task_html += f'<li class ="urgency_important">{task.get_html_url} (!)</li>'
                    elif task.urgency == Urgency.MEDIUM:
                        task_html += f'<li class ="urgency_medium">{task.get_html_url}</li>'
                    else:
                        task_html += f'<li>{task.get_html_url}</li>'


            for task in taken_tasks:
                task_volunteering = Volunteering.objects.get(task=task)
                if self.user.is_staff or self.user == task_volunteering.user:
                    task_html += f'<li class ="taken_task">{task.get_html_url} &#10003;</li>'

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
