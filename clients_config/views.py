# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from core.models import Mac
from core.models import Activation
from core.models import Server
import datetime

def gatewaysByMac(request, mac):
    print("MAC: " + mac)
    macMod = mac.replace("-", ":")
    macQuerySet = Mac.objects.filter(address = macMod)

    print(macQuerySet)
    gateways = ""
    if macQuerySet.exists():
        if macQuerySet[0].client.unrestricted:
            for gateway in Server.objects.filter(active=True).all():
                gateways += gateway.ip + ','
        else:
            activePeriods = Period.objects.filter(begin__lte = datetime.datetime.now(), end__gte = datetime.datetime.now())
            activationQuerySet = Activation.objects.filter(client=macQuerySet[0].client, period__in=activePeriods).order_by("-creation")
            if(activationQuerySet.exists()):
                for activation in activationQuerySet.all():
                    gateways += activation.supplier.ip + ','
            else:
                gateways = "Client non activé"
    else:
        print("Mac non enregistrée")
        gateways = "Mac non enregistrée"

    gateways = gateways.strip(', ')
    print(gateways)
    return HttpResponse(gateways)


def servers(request):
    querySet = Server.objects.filter(active = True).filter(rivnet = True)

    print(querySet)
    servers = ""
    if(querySet.exists()):
        for server in querySet.all():
            servers += server.alt + ","

        servers = servers.strip(",")
    else:
        print("ATTENTION !!! AUCUN SERVERS RIVNET ACTIF CONFIGURÉ !!! LES CLIENTS RISQUENT DE CORROMPRE LEUR CONFIGURATION !!!")
        servers = "Erreur ! Merci de contacter votre administrateur réseau !"
        return HttpResponse(servers, status=500)
    
    servers = servers.strip(', ')
    print(servers)

    return HttpResponse(servers)
