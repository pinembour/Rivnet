# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from core.models import Mac
from core.models import Activation
from core.models import Server

def gatewayByMac(request, mac):

    print("MAC: " + mac)

    macMod = mac.replace("-", ":")

    macQuerySet = Mac.objects.filter(address = macMod)

    print(macQuerySet)

    if(macQuerySet.exists()):

        activationQuerySet = Activation.objects.filter(client=macQuerySet[0].client).order_by("-creation")

        print(activationQuerySet)

        if(activationQuerySet.exists()):

            gateway = activationQuerySet[0].supplier.ip

        else:

            gateway = "Client non activé"

    else:

        print("Mac non enregistrée")

        gateway = "Mac non enregistrée"


    return HttpResponse(gateway)

def servers(request):

    querySet = Server.objects.filter(active = True).filter(rivnet = True)

    print(querySet)

    servers = ""

    if(querySet.exists()):

        for server in querySet.all():

            servers = server.ip + ":8000,"

        servers = servers.strip(",")

    else:

        print("ATTENTION !!! AUCUN SERVERS RIVNET ACTIF CONFIGURÉ !!! LES CLIENTS RISQUENT DE CORROMPRE LEUR CONFIGURATION !!!")

        servers = "Erreur ! Merci de contacter votre administrateur réseau !"
        return HttpResponse(servers, status=500)


    return HttpResponse(servers)
