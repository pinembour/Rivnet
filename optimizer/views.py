# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Client
from core.models import Server
from core.models import Activation

import subprocess

def __execute(command):
    command_split = str(command).split()
    return subprocess.call(command_split)

def __ping(address):
    return __execute("ping -c 1 -t 1 " + address)

@login_required(login_url='/admin/login/')
def optimize(request):

    activations = Activation.objects.all()

    _servers = Server.objects.filter(active = True).all()

    servers = {}
    i = 0
    for serv in _servers:
        r = __ping(serv.ip)
        if r == 0:
            servers[i] = serv
            i += 1

    non_optimize = activations.filter(client__optimize = False)
    #for

    log = []
    nb_servers = len(servers)
    i = 0
    optimize = activations.filter(client__optimize = True)
    for a in optimize:
        if a.time_left() > 0:
            log += [str(a.client) + ": " + str(a.supplier) + " => " + str(servers[i])]
            a.supplier = servers[i]
            a.save()

            i += 1
            if i == nb_servers:
                i = 0

    context = {}
    context["servers"] = (servers)
    context["log"] = (log)
    return render(request, 'optimizer/optimize.html', context)
