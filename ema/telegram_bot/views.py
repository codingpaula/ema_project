from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from orga.forms import BotForm
from orga.models import UserOrga

def ema_authenticate(request):
    return render(request, 'telegram_bot/start.html')

class SetupBot(SuccessMessageMixin, UpdateView):
    model = UserOrga
    form_class = BotForm
    template_name = 'telegram_bot/telegram_setup.html'
    success_message = 'Successfully saved!'
    success_url = '/bot/telegrambot'

    def get_object(self):
        return get_object_or_404(UserOrga, owner=self.request.user)
