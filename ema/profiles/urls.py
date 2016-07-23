from __future__ import absolute_import

from django.contrib.auth.views import login, logout
from django.conf.urls import url

from . import views

urlpatterns = [
    #/account/
    url(r'^$', views.account, name='account'),
    #/account/index/
    url(r'^index/$', views.index, name='index'),
    #/account/login/
    url(r'^login/$', login, name='login'),
    #/account/loggedout/
    url(r'^loggedout/$', logout, name='loggedout'),
    #/account/register/
    url(r'^register/$', views.register, name='register')
]
