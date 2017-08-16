# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.models import Port
from core.models import Client
from core.models import Supplier
from core.models import Mac
from core.models import Activation
from core.models import Forward
from core.models import Input

from . import firewall_script

@login_required(login_url='/admin/login/')
def index(request):

    context = {}
    return render(request, 'firewall/index.html', context)

@login_required(login_url='/admin/login/')
def start(request):

    context = firewall_script.start()
    return render(request, 'firewall/start.html', context)

@login_required(login_url='/admin/login/')
def stop(request):

    context = firewall_script.stop()
    return render(request, 'firewall/stop.html', context)

@login_required(login_url='/admin/login/')
def restart(request):

    context = firewall_script.restart()
    return render(request, 'firewall/restart.html', context)
