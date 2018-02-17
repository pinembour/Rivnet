#!/usr/bin/env python3
# -*- coding:utf-8 -*
#

from django.conf.urls import url

from clients_config import views

urlpatterns = [
    url(r'^gateways/(?P<mac>(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2}))$', views.gatewaysByMac, name="gatewaysByMac"),
    url(r'^servers$', views.servers, name="servers"),
    ]

