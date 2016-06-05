from __future__ import absolute_import

from django.contrib.auth.views import login, logout
from django.conf.urls import url

from . import views

urlpatterns = [
    #/account/
    url(r'^$', views.account, name='account'),
    #/account/index/
    url(r'^index/$', views.index, name='index'),
    #/account/signup/
    url(r'^signup/$', views.signup, name='signup'),
    #/account/login/
    url(r'^login/$', login, name='login'),
    #/account/loggedin/
    #url(r'^loggedin/$', views.loggedin, name='loggedin'),
    #/account/logout/
    #url(r'^logout/$', views.logout, name='logout'),
    #/account/loggedout/
    url(r'^loggedout/$', logout, name='loggedout'),
    #/account/invalid/
    #url(r'^invalid/$', views.invalid, name='invalid')
    #/account/register/
    url(r'^register/$', views.register, name='register')
]
