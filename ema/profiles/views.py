from django.shortcuts import render
from django.http import HttpResponse


def account(request):
    return render(request, 'profiles/account.html')

def signup(request):
    return render(request, 'profiles/signup.html')

def login(request):
    return render(request, 'profiles/login.html')
