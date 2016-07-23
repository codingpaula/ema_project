"""ema_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from __future__ import absolute_import

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from matrix import urls as matrix_urls
from profiles import urls as profile_urls
from profiles.views import index
from orga import urls as orga_urls

urlpatterns = [
    # startpage
    url(r'^$', index, name='startpage'),
    # account app
    url(r'^account/', include(profile_urls, namespace="profiles")),
    # matrix app
    url(r'^matrix/', include(matrix_urls, namespace="matrix")),
    # orga app
    url(r'^orga/', include(orga_urls, namespace="orga")),
    # admin tool
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# static files und speicherung static files
