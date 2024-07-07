from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from backend.forms import CustomAdminPasswordChangeForm
from backend.models.user import User


def index(request):
    return render(request, 'master.html', {'name': 'Harry'})

# original django code from https://github.com/django/django/blob/main/django/contrib/auth/views.py
class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context

class CustomAdminPasswordChangeView(PasswordContextMixin, FormView):
    form_class = CustomAdminPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    # this template is an edited version of this django original template: https://github.com/django/django/blob/main/django/contrib/admin/templates/admin/auth/user/change_password.html
    template_name = "admin_change_pw.html"
    title = _("TEST Password change")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user=request.user
        new_pw_user_id = self.kwargs["pk"]
        new_pw_user = User.objects.get(id=new_pw_user_id)
        if (
                not user.is_staff
                or (not user.is_superuser and (new_pw_user.is_superuser or new_pw_user.is_staff))
        ):
            raise PermissionDenied('Keine Berechtigung zum Ändern des Passworts')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        new_pw_user_id = self.kwargs["pk"]
        new_pw_user = User.objects.get(id=new_pw_user_id)
        #kwargs["user"] = self.request.user
        kwargs["user"] = new_pw_user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
