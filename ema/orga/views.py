from django.shortcuts import render

"""
nur ein Template View mit Informationen ueber dieses Projekt
"""
def about_ema(request):
    return render(request, 'orga/about_ema.html')

"""
das Impressum
"""
def impressum(request):
    return render(request, 'orga/impressum.html')
