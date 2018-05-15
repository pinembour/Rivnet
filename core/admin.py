# -*- coding: utf-8 -*-
from datetime import datetime
from django.utils.html import mark_safe

from django.contrib import admin

from .models import Port
from .models import Client
from .models import Server
from .models import Mac
from .models import Activation
from .models import Forward
from .models import Period
from .models import Input

class MacAdminInline(admin.TabularInline):
    model = Mac
    extra = 0


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

    inlines = [MacAdminInline,]

class ServerAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('server_name', 'client', 'ip', 'restart_firewall', 'synchronize', 'active', 'rivnet')
    list_display_links = ('server_name', 'client', 'ip')

    search_fields = ('server_name', 'client__nickname', 'client__first_name', 'client__last_name', 'ip')

    def restart_firewall(self, obj):
        return mark_safe('<a target="_blank" href="https://' + obj.alt + '/firewall/restart"><input type="button" value="Restart firewall"></input></a>')

    def synchronize(self, obj):
        if obj.master:
            return mark_safe('<a target="_blank" href="https://' + obj.alt + '/core/synchronize"><input type="button" value="Synchronize"></input></a>')
        else:
            return ""

class MacAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('client', 'address')
    list_display_links = ('client', 'address')

    search_fields = ('client__nickname', 'client__first_name', 'client__last_name', 'address')

class ActivationAdmin(admin.ModelAdmin):
    view_on_site = False

    #List parameters
    list_display = ('period', 'client', 'supplier', 'creation', 'subscription_view', 'active')
    list_display_links = ('period', 'client', 'subscription_view')

    def subscription_view(self, obj):
        return '%i €' % obj.subscription
    subscription_view.short_description = 'Subscription'

    list_editable = ('supplier', 'active')
    list_filter = ('period', 'supplier', 'active')

    search_fields = ('client__nickname', 'client__first_name', 'client__last_name', 'supplier__server_name')

    #Edit parameters
    fields = ('period', 'client', 'supplier', 'subscription', 'active')

class PeriodAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('name', 'begin', 'end', 'sum_view')
    list_display_links = ('name', 'begin', 'end')

    def sum_view(self, obj):
        return '%i €' % obj.sum()
    sum_view.short_description = "Money"

    search_fields = ('name', 'begin', 'end')

class ForwardAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('port',)
    list_display_links = ('port',)

    list_filter = ('port',)

    search_fields = ('port__name',)

class InputAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('supplier', 'port')
    list_display_links = ('supplier', 'port')

    list_filter = ('supplier', 'port')

    search_fields = ('supplier__server_name', 'port__name')


admin.site.register(Port, PortAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Mac, MacAdmin)
admin.site.register(Activation, ActivationAdmin)
admin.site.register(Forward, ForwardAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(Input, InputAdmin)

admin.site.site_header = 'Rivnet'
admin.site.site_title = 'Rivnet |'
admin.site.index_title = ''
