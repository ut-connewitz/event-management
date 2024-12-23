#import logging
from datetime import datetime, timedelta
from calendar import HTMLCalendar
from backend.models.event import Event, PastEvent
from backend.models.task import Task, State, Volunteering, TeamRestriction, Urgency
from backend.models.user import TeamMember


class Calendar(HTMLCalendar):
    def __init__(self,  user, year=None, month=None):
        self.year = year
        self.month = month
        self.user = user
        super(Calendar, self).__init__()

    def check_team_restriction(self, team_restriction, user_teams):
        if team_restriction == TeamRestriction.NONE:
            return True
        else:
            for user_team in user_teams:
                if team_restriction == TeamRestriction.LIGHT:
                    if user_team.team.name == "Licht":
                        return True
                elif team_restriction == TeamRestriction.SOUND:
                    if user_team.team.name == "Ton":
                        return True
                elif team_restriction == TeamRestriction.OFFICE:
                    if user_team.team.name == "Verwaltung":
                        return True

    #formats a days as table cell
    #filters events by day
    def formatday(self, day, events, past_events):
        events_per_day = events.filter(date__day=day)
        past_events_per_day = past_events.filter(date__day=day)
        day_content = ''

        for event in events_per_day:
            empty_task_html = f'''<div class="collapse"
                            id="{event.event_id}_tasks"
                            aria-labelledby="#{event.event_id}_tasks_header"
                            data-parent=#{event.event_id}_tasks_header>
                                <ul>
                                '''
            empty_task_html_closure = '</ul></div>'
            task_html = self.get_event_task_html(event, empty_task_html, empty_task_html_closure)


            if task_html != empty_task_html + empty_task_html_closure:
                #day_content += f'<ul>' + task_html +f'</ul>'
                day_content += f'''<li>{event.get_html_url}
                                    <br>
                                        <div id="{event.event_id}_tasks_header"
                                                <button class="btn btn-secondary btn-sm"
                                                    type="button"
                                                    data-bs-toggle="collapse"
                                                    data-bs-target="#{event.event_id}_tasks"
                                                    aria-expanded="false"
                                                    aria-controls="{event.event_id}_tasks">
                                                        Aufgaben
                                                </button>
                                        </div>
                                            {task_html}
                                    </li>'''
            else:
                day_content += f'<li>{event.get_html_url}</li>'


        for past_event in past_events_per_day:
            day_content += f'<li class="past_event">{past_event.get_html_url} </li>'

        if day!= 0:
            if day_content!='':
                return f"""<td>
                                <div class='event_day'>
                                    <span class='date'>
                                        {day}
                                    </span>
                                    <ul>
                                        {day_content}
                                    </ul>
                                </div>
                            </td>"""
            return f"""<td>
                            <div class='empty_day'>
                                <span class='date'>
                                    {day}
                                </span>
                            </div>
                        </td>"""
        return "<td><div class='other_month'></div></td>"

    def get_event_task_html(self, event, empty_task_html, empty_task_html_closure):
        free_tasks = Task.objects.filter(event=event, state=State.FREE)
        #logger = logging.getLogger(__name__) #debug
        #logger.error(str(free_tasks)) #debug
        taken_tasks = Task.objects.filter(event=event, state=State.TAKEN)
        task_html = empty_task_html
        user_teams = TeamMember.objects.filter(user=self.user)

        for task in free_tasks:
            team_restriction = task.team_restriction
            pass_team_restriction = self.check_team_restriction(team_restriction, user_teams)
            if self.user.is_staff or pass_team_restriction:
                if task.urgency == Urgency.URGENT:
                    task_html += f'<li class ="urgency_urgent">{task.get_html_url} &#9200;</li>'
                elif task.urgency == Urgency.IMPORTANT:
                    task_html += f'<li class ="urgency_important">{task.get_html_url} &#8252;</li>'
                elif task.urgency == Urgency.MEDIUM:
                    task_html += f'<li class ="urgency_medium">{task.get_html_url}</li>'
                else:
                    task_html += f'<li>{task.get_html_url}</li>'

        for task in taken_tasks:
            try:
                task_volunteering = Volunteering.objects.get(task=task)
                volunteering_user = task_volunteering.user
            except Volunteering.DoesNotExist:
                volunteering_user = None

            if self.user.is_staff or self.user == task_volunteering.user:
                task_html += f'<li class ="taken_task">{task.get_html_url} &#10003;</li>'

        task_html += empty_task_html_closure
        return task_html

    #formats a week as tr
    def formatweek(self, theweek, events, past_events):
        week_html = ''
        for day, weekday in theweek:
            week_html += self.formatday(day, events, past_events)
        return f'<tr> {week_html} </tr>'

    #formats a month as a table
    #filters events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(date__year=self.year, date__month=self.month)
        past_events = PastEvent.objects.filter(date__year=self.year, date__month=self.month)
        #calendar_html = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        calendar_html = f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        calendar_html += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
		          calendar_html += f'{self.formatweek(week, events, past_events)}\n'
        #calendar_html += f'</table>'
        return calendar_html
