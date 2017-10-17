import json
from django import forms
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

from orga.forms import OrgaForm
from orga.models import UserOrga
from matrix.views import AjaxSuccessMessageMixin


def index(request):
    """
    Startpage, link to register and login.

    redirect, falls schon eingeloggt zur Matrix
    in config-urls Datei, da host-address/
    """
    if request.user.is_authenticated():
        return redirect('/matrix/')
    else:
        form = AuthenticationForm(request)
        return render(request, 'registration/login.html', {'form': form})


# http://www.djangobook.com/en/2.0/chapter14.html
def register(request):
    """Registrierung."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('matrix:matrix'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class AjaxableSettingsResponseMixin(object):
    """
    Mixin to add AJAX support to a form.

    Must be used with an object-based FormView (e.g. CreateView)
    @source: django docs
    https://docs.djangoproject.com/en/1.8/topics/class-based-views/generic-editing/
    """

    def form_invalid(self, form):
        """Response bei Fehler."""
        response = super(AjaxableSettingsResponseMixin, self).form_invalid(form)
        # Fehler uebergeben, korrekter Statuscode fuer die Behandlung mit AJAX
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        """Response bei gueltigen Daten."""
        response = super(AjaxableSettingsResponseMixin, self).form_valid(form)
        # bei AJAX werden nur nur ein JSON-Objekt der Aufgaben uebergeben
        if self.request.is_ajax():
            urgent_axis = form.instance.urgent_axis
            user_orga_object = UserOrga.objects.filter(
                owner_id=self.request.user.id)
            response_data = json.dumps(
                [model_to_dict(instance) for instance in user_orga_object],
                cls=DjangoJSONEncoder)
            return HttpResponse(response_data, content_type="application/json")
        else:
            return response


class AccountSettings(
        AjaxableSettingsResponseMixin,
        AjaxSuccessMessageMixin,
        UpdateView):
    """
    Wird nach Login angezeigt.

    Name des Nutzers und seine Einstellungen werden angezeigt
    """

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

    # spaeter fuer die Aenderung von Passwoertern
    # def get_context_data(self, *args, **kwargs):
    #     context = super(AccountSettings, self).get_context_data(*args, **kwargs)
    #     context['passwordChange'] = PasswordChangeForm(self.request.user)
    #     return context

"""
alternativer View fuer die Account-Seite, da die Umsetzung von zwei Forms auf
einer Seite mit CBVs umstaendlich ist
"""
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

"""
Passwortaenderung als Feature geplant
"""
# TODO Passwortaenderung
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
