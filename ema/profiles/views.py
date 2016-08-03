from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

"""
startpage, link to register and login
redirect, falls schon eingeloggt zur Matrix
"""
def index(request):
    if request.user.is_authenticated():
        return redirect('/matrix')
    else: return render(request, 'profiles/index.html')

"""
wird nach Login angezeigt
Informationen ueber diesen Benutzer (bis jetzt nur Name) werden angezeigt
"""
@login_required(login_url='/account/login')
def account(request):
    return render(request, 'profiles/account.html')

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
            login(request, new_user)
            return HttpResponseRedirect(reverse('profiles:account'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
