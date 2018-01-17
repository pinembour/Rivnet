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
        return mark_safe('<a target="_blank" href="http://' + obj.ip + '/firewall/restart"><input type="button" value="Restart firewall"></input></a>')

    def synchronize(self, obj):
        return mark_safe('<a target="_blank" href="http://' + obj.ip + '/core/synchronize"><input type="button" value="Synchronize"></input></a>')

class MacAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('client', 'address')
    list_display_links = ('client', 'address')

    search_fields = ('client__nickname', 'client__first_name', 'client__last_name', 'address')

class ActivationAdmin(admin.ModelAdmin):
    view_on_site = False

    #List parameters
    list_display = ('client', 'supplier', 'creation', 'duration_view', 'subscription_view', 'active', 'time_left_view')
    list_display_links = ('client', 'duration_view', 'subscription_view')

    def duration_view(self, obj):
        return '%i month(s)' % obj.duration
    duration_view.short_description = 'Duration'

    def subscription_view(self, obj):
        return '%i €' % obj.subscription
    subscription_view.short_description = 'Subscription'

    def time_left_view(self, obj):
        return '%i month(s) ' % (obj.time_left())
    time_left_view.short_description = 'Time left'

    list_editable = ('supplier', 'active')
    list_filter = ('supplier', 'active')

    search_fields = ('client__nickname', 'client__first_name', 'client__last_name', 'supplier__server_name')

    #Edit parameters
    fields = ('client', 'supplier', 'duration', 'subscription', 'active')

class ForwardAdmin(admin.ModelAdmin):
    view_on_site = False

    list_display = ('supplier', 'port')
    list_display_links = ('supplier', 'port')

    list_filter = ('supplier', 'port')

    search_fields = ('supplier__server_name', 'port__name')

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
admin.site.register(Input, InputAdmin)

admin.site.site_header = 'Rivnet'
admin.site.site_title = 'Rivnet |'
admin.site.index_title = ''
