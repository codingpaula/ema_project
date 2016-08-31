from __future__ import absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    # /bot/start/
    url(r'^start$', views.ema_authenticate, name='start')
]
