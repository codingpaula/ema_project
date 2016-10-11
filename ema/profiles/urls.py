from __future__ import absolute_import

from django.contrib.auth.views import login, logout, password_change
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from .views import AccountSettings

urlpatterns = [
    #/account/
    url(r'^$', login_required(AccountSettings.as_view()), name='account'),
    #/account/login/
    url(r'^login/$', login, name='login'),
    #/account/loggedout/
    url(r'^loggedout/$', logout, name='loggedout'),
    #/account/register/
    url(r'^register/$', views.register, name='register'),
    #/account/passwordchange/
    # url(r'^passwordchange/$', views.update_password, name="passwordchange")
]
