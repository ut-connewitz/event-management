from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from backend.models.user import User, UTMember
#from .forms import AccountForm

class ProfileHub(LoginRequiredMixin, TemplateView):
    template_name = 'profile_page/profile_hub.html'

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_pk = user.pk

        context['user_pk'] = user_pk

        return context

class Account(LoginRequiredMixin, UpdateView):
    model = User
    #if self.request.user.is_staff:
        #fields = '__all__'
    #else:
    fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    template_name ='profile_page/account.html'

    # first built in method that is called when the view is used
    # used here to check if the user instance given by the url belongs to the logged in user
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().pk != request.user.id:
            raise Http404('Falscher Account.')
        return super(Account, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        membership_number = None
        try:
            member = UTMember.objects.get(user=user)
        except UTMember.DoesNotExist:
            member = None

        if member != None:
            membership_number = member.member_number

        context['membership_number'] = membership_number

        return context


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
