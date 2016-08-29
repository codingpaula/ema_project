from __future__ import absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    #/orga/about_ema
    url(r'^about_ema/$', views.about_ema, name='about_ema'),
    #/orga/impressum
    url(r'^impressum/$', views.impressum, name='impressum'),
    #/orga/help
    url(r'^help/$', views.help, name='help')
]
