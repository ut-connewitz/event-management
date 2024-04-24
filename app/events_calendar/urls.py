from django.urls import path
from . import views

app_name = 'events_calendar'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
]
