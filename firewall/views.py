# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from core.models import Port
from core.models import Client
from core.models import Supplier
from core.models import Mac
from core.models import Activation
from core.models import Forward
from core.models import Input

from . import firewall_script
from . import settings

def __context():

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
        supplier = Supplier.objects.get(server_name = settings.server_name)
    except Supplier.DoesNotExist:
        return HttpResponse("Settings are misconfigured")

    res["local_tcp_ports"] = []
    res["local_udp_ports"] = []

    for input in supplier.inputs.all():
        port = input.port

        if port.tcp:
            res["local_tcp_ports"].append(port.value)
        if port.udp:
            res["local_udp_ports"].append(port.value)

    res["forward_tcp_ports"] = []
    res["forward_udp_ports"] = []

    for forward in supplier.forwards.all():
        port = forward.port

        if port.tcp:
            res["forward_tcp_ports"].append(port.value)
        if port.udp:
            res["forward_udp_ports"].append(port.value)

    cotisations = Activation.objects.all()

    res["clients"] = []
    for cotis in cotisations:
        client = cotis.client

        if int(cotis.time_left()) >= 0:
            macs = []

            for mac in client.macs.all():
                macs.append(mac.address)

            res["clients"].append({
                "name": str(client),
                "macs": macs,
                "admin": client.unrestricted
            })

    return res

@login_required(login_url='/admin/login/')
def index(request):

    context = {}
    return render(request, 'firewall/index.html', context)

@login_required(login_url='/admin/login/')
def start(request):

    settings = __context()
    context = firewall_script.start(settings["wan_int"], settings["wan_ip"], settings["wan_r"], settings["lan_int"], settings["lan_ip"], settings["lan_r"], settings["lan_admin_int"], settings["lan_admin_ip"], settings["lan_admin_r"], settings["local_tcp_ports"], settings["local_udp_ports"], settings["forward_tcp_ports"], settings["forward_udp_ports"], settings["clients"])
    return render(request, 'firewall/start.html', context)

@login_required(login_url='/admin/login/')
def stop(request):

    context = firewall_script.stop()
    return render(request, 'firewall/stop.html', context)

@login_required(login_url='/admin/login/')
def restart(request):

    settings = __context()
    context = firewall_script.restart(settings["wan_int"], settings["wan_ip"], settings["wan_r"], settings["lan_int"], settings["lan_ip"], settings["lan_r"], settings["lan_admin_int"], settings["lan_admin_ip"], settings["lan_admin_r"], settings["local_tcp_ports"], settings["local_udp_ports"], settings["forward_tcp_ports"], settings["forward_udp_ports"], settings["clients"])
    return render(request, 'firewall/restart.html', context)
