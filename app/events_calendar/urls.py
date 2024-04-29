from django.urls import path
from . import views

# for class based views the login_required decorator can also be implemented here
# e.g. path('calendar/', login_required(views.CalendarView.as_view()), name='calendar'),
# but the ussage of the mixin within views.py seems more convenient
app_name = 'events_calendar'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event_day/new/', views.event_day, name='event_day_new'),
    path('event_day/edit/(?<event_day_id>\d+)/', views.event_day, name='event_day_edit'),
    path('task/edit/(?<task_id>\d+)/', views.task, name='task_edit'),
]
