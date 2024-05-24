from django.urls import path
from . import views

# for class based views the login_required decorator can also be implemented here
# e.g. path('calendar/', login_required(views.CalendarView.as_view()), name='calendar'),
# but the ussage of the mixin within views.py seems more convenient
app_name = 'profile_page'
urlpatterns = [
    path('hub/', views.ProfileHub.as_view(), name='hub'),
    path('account/<int:pk>/', views.Account.as_view(), name='account'),
    path('adress/edit/<int:pk>/', views.UpdateAdress.as_view(), name='adress_edit'),
    path('adress/create/', views.CreateAdress.as_view(), name='adress_create'),
]
