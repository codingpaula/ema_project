from __future__ import absolute_import

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .views import SetupBot

urlpatterns = [
    # /bot/start/
    url(r'^start/$', views.ema_authenticate, name='start'),
    # /bot/
    url(r'^telegrambot/$', login_required(SetupBot.as_view()), name='setup')
]
