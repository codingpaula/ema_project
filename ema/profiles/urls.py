from __future__ import absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    #/account/
    url(r'^$', views.account, name='account'),
    #/account/signup/
    url(r'^signup/$', views.signup, name='signup'),
    #/account/login/
    url(r'^login/$', views.login, name='login')
]
