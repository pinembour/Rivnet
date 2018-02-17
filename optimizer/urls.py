#!/usr/bin/env python3
# -*- coding:utf-8 -*
#

from django.conf.urls import url

from optimizer import views

urlpatterns = [
    url(r'^optimize$', views.optimize, name='optimize'),
    url(r'^status$', views.status, name='status'),
]

