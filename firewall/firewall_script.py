#!/usr/bin/env python3
# -*- coding:utf-8 -*
#
import subprocess

def __execute(command):
    command = command.split()
    return subprocess.check_output(command)

def __init():
    res = ""
    #res += __execute('')
    res += __execute('echo 1 > /proc/sys/net/ipv4/ip_forward')
    res += __execute('echo 0 > /proc/sys/net/ipv6/conf/all/forwarding')

    res += __execute('iptables -P INPUT DROP')
    res += __execute('iptables -P FORWARD DROP')

    res += __execute('iptables -N INVALID')

    res += __execute('iptables -A INPUT -i lo -j ACCEPT')
    return res

def start():
    return { 'start_log': str(__init()) }

def stop():
    return { 'stop_log': 'stoped' }

def restart():
    return dict(stop().items() + start().items())
