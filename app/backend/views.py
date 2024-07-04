from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from backend.forms import CustomAdminPasswordChangeForm


def index(request):
    return render(request, 'master.html', {'name': 'Harry'})


class CustomAdminPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomAdminPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    #template_name = 'accounts/password_change/password_admin_change.html'
    title = "Test PW"

    def dispatch(self, request, *args, **kwargs):
        #user = kwargs["user"]
        if (
            not self.request.user.is_staff
            #or (not self.request.user.is_superuser and user.is_superuser)
        ):
            raise PermissionDenied('Keine Berechtigung zum Ändern des Passworts')
        return super(CustomAdminPasswordChangeView, self).dispatch(request, *args, **kwargs)
