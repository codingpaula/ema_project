from django.shortcuts import render

def about_ema(request):
    return render(request, 'orga/about_ema.html')

def impressum(request):
    return render(request, 'orga/impressum.html')
