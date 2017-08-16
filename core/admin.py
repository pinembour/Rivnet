# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib import admin

from .models import Port
from .models import Client
from .models import Supplier
from .models import Mac
from .models import Activation
from .models import Forward
from .models import Input

class PortAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('name', 'value', 'tcp', 'udp')
    list_display_links = ('name',)

    list_editable = ('value', 'tcp', 'udp')

    list_filter = ('tcp', 'udp')

    search_fields = ('name', 'value')

class ClientAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('nickname', 'first_name', 'last_name', 'unrestricted')
    list_display_links = ('nickname', 'first_name', 'last_name', 'unrestricted')

    list_filter = ('unrestricted',)

    search_fields = ('nickname', 'first_name', 'last_name')

class SupplierAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('server_name', 'client', 'ip')
    list_display_links = ('server_name', 'client', 'ip')

    search_fields = ('server_name', 'client', 'ip')

class MacAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('client', 'address')
    list_display_links = ('client', 'address')

    search_fields = ('client', 'address')

class ActivationAdmin(admin.ModelAdmin):
    view_on_site = False

    #List parameters
    list_display = ('client', 'supplier', 'creation', 'duration_view', 'subscription_view', 'active', 'time_left_view')
    list_display_links = ('client', 'supplier', 'duration_view', 'subscription_view')

    def duration_view(self, obj):
        return '%i month(s)' % obj.duration
    duration_view.short_description = 'Duration'

    def subscription_view(self, obj):
        return '%i €' % obj.subscription
    subscription_view.short_description = 'Subscription'

    def time_left_view(self, obj):
        return '%i month(s) ' % (obj.creation.month + obj.duration - datetime.now().date().month)
    time_left_view.short_description = 'Time left'

    list_editable = ('active',)
    list_filter = ('supplier', 'active')

    search_fields = ('client', 'supplier')

    #Edit parameters
    fields = ('client', 'supplier', 'duration', 'subscription', 'active')

class ForwardAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('supplier', 'port')
    list_display_links = ('supplier', 'port')

    list_filter = ('supplier', 'port')

    search_fields = ('supplier', 'port')

class InputAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('supplier', 'port')
    list_display_links = ('supplier', 'port')

    list_filter = ('supplier', 'port')

    search_fields = ('supplier', 'port')


admin.site.register(Port, PortAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Mac, MacAdmin)
admin.site.register(Activation, ActivationAdmin)
admin.site.register(Forward, ForwardAdmin)
admin.site.register(Input, InputAdmin)
