from django.urls import path
from . import views

app_name = 'events_calendar'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event_day/new/', views.event_day, name='event_day_new'),
    path('event_day/edit/(?<event_day_id>\d+)/', views.event_day, name='event_day_edit'),
]
