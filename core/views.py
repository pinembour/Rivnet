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

def __command(ip, directory_src, directory_dst):
    return "scp -i /home/rivnet/.ssh/id_rsa " + directory_src + "/db.sqlite3 rivnet@" + ip + ":" + directory_dst + "/db.sqlite3"

def __synchronize(server, master):
    try:
        __execute(__command(server.ip, master.install_directory, server.install_directory))
        return server.server_name + ": Synchronized via Lan"
    except Exception as e1:
        try:
            if(server.alt):
                __execute(__command(server.alt, master.install_directory, server.install_directory))
                return server.server_name + ": Failed synchronization via Lan : " + str(e1) + "Synchronized via Internet"
            else:
                return server.server_name + ": Failed synchronization via Lan : " + str(e1)
        except Exception as e2:
            return server.server_name + ": Failed synchronization via Lan : " + str(e1) + "Failed synchronization via Internet : " + str(e2)

def __synchronize_all(master):
    from .models import Server
    res = []
    for server in Server.objects.filter(rivnet = True).exclude(server_name = settings.server_name):
        res += [__synchronize(server, master)]
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
        context['log'] = __synchronize_all(server)
    else:
        context['log'] = "This server is not Master"

    return render(request, 'core/synchronize.html', context)

@login_required(login_url='/admin/login/')
def money(request):

    total = Activation.objects.filter(client__unrestricted=False).aggregate(Sum('subscription'))['subscription__sum']

    message = "Total = " + str(total)

    return HttpResponse(message)
