# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

class FirewallConfig(AppConfig):
    name = 'firewall'

    def ready(self):
        #url = 'http://wbsapi.withings.net/[service_name]?action=[action_name]&[parameters]'
        #serialized_data = urllib2.urlopen(url).read()
        pass
