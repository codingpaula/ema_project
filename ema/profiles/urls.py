from __future__ import absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    #/account/
    url(r'^$', views.account, name='account')
]
