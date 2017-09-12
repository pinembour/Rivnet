#!/usr/bin/env python3
# -*- coding:utf-8 -*
#

from django.conf.urls import url

from core import views

urlpatterns = [
    url(r'^synchronize$', views.sync, name='synchronize'),
    url(r'^money$', views.money, name='money'),
]

