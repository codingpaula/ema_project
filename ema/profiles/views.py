from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login')
def account(request):
    return render(request, 'profiles/account.html')

def signup(request):
    return render(request, 'profiles/signup.html')

def loggingin(request):
    return render(request, 'profiles/login.html')

def index(request):
    return render(request, 'profiles/index.html')

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
