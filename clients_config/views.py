# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from core.models import Mac
from core.models import Activation

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
