from django.urls import path

from . import views

app_name="backend"

urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'admin/backend/user/<int:pk>/password',
        views.CustomPasswordChangeView.as_view(),
        name='password',
    ),
]
