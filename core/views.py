from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Server

import subprocess

from . import settings

def __execute(command, shell=False):
    command_split = str(command).split()
    if shell:
        return [command + ": OK: " + str(subprocess.check_output(command_split, shell=True))]
    else:
        return [command + ": OK: " + str(subprocess.check_output(command_split))]

def __command(ip):
    return "scp -i /home/rivnet/.ssh/id_rsa /opt/rivnet/db.sqlite3 rivnet@" + ip + ":/opt/rivnet/db.sqlite3"

def __synchronize(ip, ip_alt):
    try:
        __execute(__command(ip))
    except Exception:
        __execute(__command(ip_alt))

def __synchronize_all():
    from .models import Server
    for server in Server.objects.filter(rivnet = True).filter(active = True):
        __synchronize(server.ip, server.alt)


@login_required(login_url='/admin/login/')
def sync(request):
    message = ""

    if(settings.master):
        print("Synchronization....")
        __synchronize_all()
        message = "HI ! <br /> ok."
    else:
        message = "This server is not Master"

    return HttpResponse(message)
