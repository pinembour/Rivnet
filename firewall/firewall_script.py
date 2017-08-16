#!/usr/bin/env python3
# -*- coding:utf-8 -*
#
import subprocess

def __execute(command):
    command_split = command.split()
    return [command + ": OK: " + str(subprocess.check_output(command_split))]

def __init(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports):
    res = []
    res += __execute('echo 1 > /proc/sys/net/ipv4/ip_forward')
    res += __execute('echo 0 > /proc/sys/net/ipv6/conf/all/forwarding')

    res += __execute('iptables -P INPUT DROP')
    res += __execute('iptables -P FORWARD DROP')

    res += __execute('iptables -N INVALID')

    res += __execute('iptables -A INPUT -i lo -j ACCEPT')

    #Local services
    res += __execute('iptables -A INPUT -p tcp -m multiport --dports ' + local_tcp_ports + ' -m state --state NEW -j ACCEPT')
    res += __execute('iptables -A INPUT -p udp -m multiport --dports ' + local_udp_ports + ' -m state --state NEW -j ACCEPT')

    # ICMP : ping request
    res += __execute('iptables -A INPUT -p icmp -j ACCEPT')

    # Don't touch to the established connections !
    # 'state' module, obsolete but still used
    res += __execute('iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT')
    res += __execute('iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT')
    # new module. 'conntrack' instead of 'state'
    res += __execute('iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
    res += __execute('iptables -A OUTPUT -m conntrack --ctstate NEW,RELATED,ESTABLISHED -j ACCEPT')

    # Routing Aldebaran
    res += __execute('iptables -A FORWARD -i ' + lan_admin_int + ' -j ACCEPT')
    res += __execute('iptables -A POSTROUTING -t nat -o ' + wan_int + ' -j MASQUERADE')

    # Routing Wan to Lan network
    res += __execute('iptables -A FORWARD -i ' + wan_int + ' -j ACCEPT')
    res += __execute('iptables -A POSTROUTING -t nat -o ' + lan_int + ' -j MASQUERADE')

    # Port forwarding rivlink's irc
    res += __execute('iptables -A PREROUTING -t nat -i ' + wan_int + ' -p tcp --dport 6667 -j DNAT --to 10.20.0.3:6667')
    res += __execute('iptables -A FORWARD -p tcp --dport 6667 -j ACCEPT')
    res += __execute('iptables -A PREROUTING -t nat -i ' + wan_int + ' -p tcp --dport 6668 -j DNAT --to 10.20.0.3:6668')
    res += __execute('iptables -A FORWARD -p tcp --dport 6668 -j ACCEPT')

    #VPN
    res += __execute('iptables -A FORWARD -p tcp -s 10.8.0.0/24 -j ACCEPT')
    res += __execute('iptables -A POSTROUTING -t nat -s 10.8.0.0/24 -o ' + wan_int + ' -j MASQUERADE')
    res += __execute('iptables -A POSTROUTING -t nat -s 10.8.0.0/24 -o ' + lan_int + ' -j MASQUERADE')

    return res

def route():

    res = []

    return res

def finalize(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports):

    # NAT
    res = []
    res += __execute('iptables -t nat -A POSTROUTING -j SNAT -o ' + WAN + ' --to-source ' + WAN_IP)

    res += __execute('iptables -A INVALID -j LOG --log-prefix "[===========================] "')
    res += __execute('iptables -A INVALID -j DROP')

    return res

def start(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports):

    res = __init(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports)
    res += route(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports, clients)
    res += finalize(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports)

    return { 'start_log': res }

def stop():

    res = ""

    # Kernel stuff
    res += __execute('echo 1 > /proc/sys/net/ipv4/ip_forward')
    res += __execute('echo 0 > /proc/sys/net/ipv6/conf/all/forwarding')

    # Default policy
    res += __execute('iptables  -P INPUT ACCEPT')
    res += __execute('iptables  -P OUTPUT ACCEPT')
    res += __execute('iptables  -P FORWARD ACCEPT')

    res += __execute('iptables -t nat -P PREROUTING ACCEPT')
    res += __execute('iptables -t nat -P POSTROUTING ACCEPT')
    res += __execute('iptables -t nat -P OUTPUT ACCEPT')

    # Flush
    res += __execute('iptables  -F INPUT')
    res += __execute('iptables  -F OUTPUT')
    res += __execute('iptables  -F FORWARD')
    res += __execute('iptables  -t nat -F')

    # Delete chains
    res += __execute('iptables  -F INVALID')
    res += __execute('iptables  -X INVALID')

    return { 'stop_log': res }

def restart(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports):
    return dict(stop().items() + start(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports).items())
