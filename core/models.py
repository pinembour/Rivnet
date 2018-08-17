#!/usr/bin/env python3
# -*- coding:utf-8 -*
#

from datetime import datetime
from datetime import timedelta

from django.db import models
from django.db.models import Q, Sum
from django.dispatch import receiver
import unicodedata

class Port(models.Model):
    name = models.CharField(max_length=10, blank=False)
    value = models.CharField(max_length=100, blank=False)
    tcp = models.BooleanField(default=True, blank=False)
    udp = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return (self.name)

class Period(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)
    begin = models.DateField(null=False, blank=False)
    end = models.DateField(null=False, blank=False)

    def sum(self):
        total = Activation.objects.filter(period=self).aggregate(total=Sum("subscription"))['total']
        if total == None:
            return 0
        else:
            return total


    def __str__(self):
        return (self.name)

class Client(models.Model):
    nickname = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    unrestricted = models.BooleanField(default=False, null=False, blank=False)
    optimize = models.BooleanField(default=True, null=False, blank=False)


    @staticmethod
    def search(pattern):
        return Client.objects.filter(Q(surnom=pattern) | Q(nom=pattern) | Q(prenom=pattern))

    def get_absolute_url(self):
        return reverse('client_edit', kwargs={'pk': self.pk})

    def __str__(self):
        identifier = self.nickname if self.nickname else (self.first_name + self.last_name)
        identifier = str(unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore'))
        identifier.replace(" ", "")
        identifier.replace("-", "")
        identifier.replace("_", "")
        identifier.replace("@", "a")
        identifier.replace(";", "")
        identifier = identifier.strip("b\'")

        return identifier

class Server(models.Model):
    master = models.BooleanField(default=False, null=False)
    ip = models.CharField(max_length=32, unique=True, blank=False)
    alt = models.CharField(max_length=32, blank=True, default="")
    server_name = models.CharField(max_length=50, unique=True, blank=False)
    client = models.ForeignKey(Client, models.CASCADE, null=False)
    rivnet = models.BooleanField(default=True, null=False)
    active = models.BooleanField(default=True, null=False)
    wan_int = models.CharField(max_length=32, null=False)
    wan_ip = models.CharField(max_length=32, null=False)
    wan_net = models.CharField(max_length=32, null=False)
    lan_int = models.CharField(max_length=32, null=False)
    lan_ip = models.CharField(max_length=32, null=False)
    lan_net = models.CharField(max_length=32, null=False)
    lan_admin_int = models.CharField(max_length=32, null=False)
    lan_admin_ip = models.CharField(max_length=32, null=False)
    lan_admin_net = models.CharField(max_length=32, null=False)

    def getTotalActivations(self):
        return len(self.activation_set.all())

    def __str__(self):
        return self.server_name + " (" + str(self.client) + ")"

class Mac(models.Model):
    address = models.CharField(max_length=32, unique=True, blank=False)

    client = models.ForeignKey(Client, models.CASCADE, null=False, related_name="macs");

    def __str__(self):
        return str(self.client) + " : " + self.address

    def save(self, *args, **kwargs):

        self.address = self.address.replace("-", ":")
        self.address = self.address[:17]

        super(Mac, self).save(*args, **kwargs)

class Activation(models.Model):
    subscription = models.IntegerField(default=25, null=False)
    active = models.BooleanField(default=True, null=False)

    client = models.ForeignKey(Client, models.CASCADE, null=False, unique=False)
    supplier = models.ForeignKey(Server, models.CASCADE, default=0, null=False)

    period = models.ForeignKey(Period, models.CASCADE, null=False)
    creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return  str(self.period) + " - " + str(self.supplier) + ": " + str(self.client)

class Forward(models.Model):
    port = models.ForeignKey(Port, models.CASCADE, null=False)

    def __str__(self):
        return (str(self.port))

class Input(models.Model):
    port = models.ForeignKey(Port, models.CASCADE, null=False)
    supplier = models.ForeignKey(Server, models.CASCADE, null=False, related_name="inputs")

    def __str__(self):
        return (str(self.supplier) + ": " + str(self.port))

