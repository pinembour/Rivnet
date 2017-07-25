#!/usr/bin/env python3
# -*- coding:utf-8 -*
#

from django.conf.urls import url

from firewall import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start$', views.start, name='start'),
    url(r'^stop$', views.stop, name='stop'),
    url(r'^restart$', views.restart, name='restart'),
]

