from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Sum

from .models import Server
from .models import Activation

import subprocess

from core import settings

def __execute(command, shell=False):
    command_split = str(command).split()
    if shell:
        return [command + ": OK: " + str(subprocess.check_output(command_split, shell=True))]
    else:
        return [command + ": OK: " + str(subprocess.check_output(command_split))]

def __command(ip):
    return "scp -i /home/rivnet/.ssh/id_rsa /opt/rivnet/db.sqlite3 rivnet@" + ip + ":/opt/rivnet/db.sqlite3"

def __synchronize(server):
    try:
        __execute(__command(server.ip))
        return server.server_name + ": Synchronized"
    except Exception as e:
        return server.server_name + ": Failed: " + str(e)


def __synchronize_all():
    from .models import Server
    res = []
    for server in Server.objects.filter(rivnet = True, active = True):
        res += [__synchronize(server)]
    return res

@login_required(login_url='/admin/login/')
def sync(request):
    context = {}

    server = None
    try:
        server = Server.objects.get(server_name = settings.server_name)
    except Server.DoesNotExist:
        print("Settings are misconfigured")
        return HttpResponse("Settings are misconfigured")

    if(server.master):
        print("Synchronization....")
        context['log'] = __synchronize_all()
    else:
        context['log'] = "This server is not Master"

    return render(request, 'core/synchronize.html', context)

@login_required(login_url='/admin/login/')
def money(request):

    total = Activation.objects.filter(client__unrestricted=False).aggregate(Sum('subscription'))['subscription__sum']

    message = "Total = " + str(total)

    return HttpResponse(message)
