# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import urllib.request
import subprocess

from core.models import Client
from core.models import Server
from core.models import Period
from core.models import Activation

def __execute(command):
    command_split = str(command).split()
    return subprocess.call(command_split)

def __pingLocal(address):
    return __execute("ping -c 1 -t 1 " + address)

def __ping(address):
    return __execute("ping -c 1 " + address)

def __testInternetStatus(address):
    
    try:
        r = urllib.request.urlopen('https://' + address + "/optimizer/status")
        print(r.read())
    except:
        return False
    
    return True

@login_required(login_url='/admin/login/')
def optimize(request):

    _servers = Server.objects.filter(active = True).all()

    servers = {}
    i = 0
    for serv in _servers:
        r = __pingLocal(serv.ip)
        if r == 0:
            #Let's do status test
            if __testInternetStatus("admin.glargh.fr"):
                servers[i] = serv
                i += 1
    
    log = []
    if i > 0:

        nb_servers = len(servers)
        i = 0
        activePeriods = Period.objects.filter(begin__lte = datetime.datetime.now(), end__gte = datetime.datetime.now())
        optimize = Activation.objects.filter(client__optimize=True, period__in=activePeriods).order_by("-creation")
        for a in optimize:
            log += [str(a.client) + ": " + str(a.supplier) + " => " + str(servers[i])]
            a.supplier = servers[i]
            a.save()

            i += 1
            if i == nb_servers:
                i = 0
    else:
        log += "No server available"

    context = {}
    context["servers"] = (servers)
    context["log"] = (log)
    return render(request, 'optimizer/optimize.html', context)


def status(request):
    r = __ping("fsf.org")
    print(r)
    if r != 0:
        return HttpResponse("Can't reach Internet", status=500)

    return HttpResponse(r)
