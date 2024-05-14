from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from backend.models.user import User
from .forms import AccountForm

class ProfileHub(LoginRequiredMixin, TemplateView):
    template_name = 'profile_page/profile_hub.html'

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_pk = user.pk

        #account_url = 'profile:account/'+str(user.pk)+'/'
        account_url = user.get_absolute_url

        context['account_url'] = account_url
        context['user_pk'] = user_pk


        return context

class Account(LoginRequiredMixin, UpdateView):
    model = User
    fields = '__all__'

    template_name ='profile_page/account.html'

#    def init_account_form(request):
#        user_instance = request.user

#        account_form = AccountForm(request.POST or None, instance=user_instance)

#        if request.POST and form.is_valid():
#            form.save()
#            return HttpResponseRedirect(reverse('profile:hub'))
#        return render(request, 'profile_page/account.html', {'form':account_form})

#    def get_context_data(self, **kwargs,):
#        context = super().get_context_data(**kwargs)


#        context['account_form'] = account_form

#        return context
