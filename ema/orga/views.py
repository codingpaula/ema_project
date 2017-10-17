"""Views for not so important sites."""
from django.shortcuts import render


def about_ema(request):
    """Nur ein Template View mit Informationen ueber dieses Projekt."""
    return render(request, 'orga/about_ema.html')


def impressum(request):
    """Das Impressum."""
    return render(request, 'orga/impressum.html')


def help(request):
    """Hilfe-Seite = Anleitung zur Benutzung."""
    return render(request, 'orga/help.html')
