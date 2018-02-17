# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from core.models import Port
from core.models import Client
from core.models import Period 
from core.models import Server
from core.models import Mac
from core.models import Activation
from core.models import Forward
from core.models import Input

from . import firewall_script
from . import settings

def __getContext():

    print("extracting data")

    res = {}

    res["wan_int"] = settings.wan_int
    res["wan_ip"] = settings.wan_ip
    res["wan_r"] = settings.wan_r

    res["lan_int"] = settings.lan_int
    res["lan_ip"] = settings.lan_ip
    res["lan_r"] = settings.lan_r

    res["lan_admin_int"] = settings.lan_admin_int
    res["lan_admin_ip"] = settings.lan_admin_ip
    res["lan_admin_r"] = settings.lan_admin_r


    supplier = None
    try:
        supplier = Server.objects.get(server_name = settings.server_name)
    except Server.DoesNotExist:
        print("Settings are misconfigured")
        return HttpResponse("Settings are misconfigured")

    res["local_tcp_ports"] = []
    res["local_udp_ports"] = []

    for input in supplier.inputs.all():
        port = input.port

        print(port)
        if port.tcp:
            res["local_tcp_ports"].append(port.value)
        if port.udp:
            res["local_udp_ports"].append(port.value)

    res["forward_tcp_ports"] = []
    res["forward_udp_ports"] = []

    for forward in Forward.objects.all():
        port = forward.port

        if port.tcp:
            res["forward_tcp_ports"].append(port.value)
        if port.udp:
            res["forward_udp_ports"].append(port.value)

    activePeriods = Period.objects.filter(begin__lte = datetime.now(), end__gte = datetime.now())
    cotisations = Activation.objects.filter(period__in=activePeriods).order_by("-creation")

    res["clients"] = []
    for cotis in cotisations:
        client = cotis.client
        macs = []

        for mac in client.macs.all():
            macs.append(mac.address)

        res["clients"].append({
            "name": str(client),
            "macs": macs,
            "admin": client.unrestricted
        })
    print("extracting data ok")
    print(res)

    return res

@login_required(login_url='/admin/login/')
def index(request):

    context = {}
    return render(request, 'firewall/index.html', context)

@login_required(login_url='/admin/login/')
def start(request):

    settings = __context()
    context = firewall_script.start(settings)
    return render(request, 'firewall/start.html', context)

@login_required(login_url='/admin/login/')
def stop(request):

    context = firewall_script.stop()
    return render(request, 'firewall/stop.html', context)

@login_required(login_url='/admin/login/')
def restart(request):

    settings = __getContext()
    context = firewall_script.restart(settings)
    return render(request, 'firewall/restart.html', context)
