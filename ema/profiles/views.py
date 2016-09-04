from django import forms
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orga.forms import OrgaForm
from orga.models import UserOrga
"""
startpage, link to register and login
redirect, falls schon eingeloggt zur Matrix
"""
def index(request):
    if request.user.is_authenticated():
        return redirect('/matrix/')
    else:
        form = AuthenticationForm(request)
        return render(request, 'registration/login.html', {'form': form})

"""
wird nach Login angezeigt
Informationen ueber diesen Benutzer (bis jetzt nur Name) werden angezeigt
"""
@login_required()
def account(request):
    form = OrgaForm(user=request.user)
    user_orga = get_object_or_404(UserOrga, owner=request.user)
    return render(request, 'profiles/account.html', {'form': form, 'user_orga': user_orga})

class AccountSettings(SuccessMessageMixin, UpdateView):
    model = UserOrga
    form_class = OrgaForm
    template_name = 'profiles/account.html'
    success_url = '/account/'
    success_message = "Successfully saved!"

    def get_object(self):
        return get_object_or_404(UserOrga, owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(AccountSettings, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
         context = super(AccountSettings, self).get_context_data(*args, **kwargs)
         context['passwordChange'] = PasswordChangeForm(self.request.user)
         return context

@login_required()
def settings(request):
    if request.method == 'POST':
        form = OrgaForm(request.POST, request.user)
        if form.is_valid():
            form.save()
            messages.info("Successfully saved!")
            return HttpResponseRedirect(reverse('profiles:account'))
    else:
        form = OrgaForm(request.user)
        passwordChange = PasswordChangeForm(request.user)
        settings = get_object_or_404(UserOrga, owner=request.user)
        return render(request, 'profiles/account.html',
                    {'form': form,
                    'passwordChange': passwordChange,
                    'settings': settings})

def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.info(request, "Password successfully changed!")
            return HttpResponseRedirect(reverse('profiles:account'))
        else:
            messages.info(request, "error")
            return HttpResponseRedirect(reverse('profiles:account'))

"""
Registrierung
"""
# http://www.djangobook.com/en/2.0/chapter14.html
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            user_settings = UserOrga(owner=new_user)
            user_settings.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse('profiles:account'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
