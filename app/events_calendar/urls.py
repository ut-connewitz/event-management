from django.urls import path
from . import views

# for class based views the login_required decorator can also be implemented here
# e.g. path('calendar/', login_required(views.CalendarView.as_view()), name='calendar'),
# but the ussage of the mixin within views.py seems more convenient
app_name = 'events_calendar'
urlpatterns = [
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/(?<event_id>\d+)/', views.event, name='event_edit'),
    path('task/edit/(?<task_id>\d+)/', views.task, name='task_edit'),
    path('task/new/', views.task, name='task_new'),
    path('task/new/<int:event_id>', views.task, name='event_task_new'),
]
