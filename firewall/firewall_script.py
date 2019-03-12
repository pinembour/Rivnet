#!/usr/bin/env python3
# -*- coding:utf-8 -*
#
import subprocess

def __execute(command, shell=False):
    command_split = str(command).split()
    if shell:
        return [command + ": OK: " + str(subprocess.check_output(command_split, shell=True))]
    else:
        return [command + ": OK: " + str(subprocess.check_output(command_split))]
    return [command]


def __sub(tab, size):
    res = []
    temp = []
    i = 0
    for a in tab:
        temp.append(a)
        i += 1
        if i == size:
            i = 0
            res.append(temp)
            temp = []
    if i > 0:
        res.append(temp)

    return res


def start(kwargs):

    res = []
    res += __execute('echo 1 > /proc/sys/net/ipv4/ip_forward')
    res += __execute('echo 0 > /proc/sys/net/ipv6/conf/all/forwarding')

    res += __execute('iptables -P INPUT DROP')
    res += __execute('iptables -P FORWARD DROP')

    res += __execute('iptables -A INPUT-RIVNET -i lo -j ACCEPT')

    res += __execute('iptables -A INPUT-RIVNET -p tcp -m multiport --dports 22 -m state --state NEW -j ACCEPT')
    res += __execute('iptables -A INPUT-RIVNET -i wlx00c0ca84a3dd -p udp -m multiport --dports 67,68 -m state --state NEW -j ACCEPT')

    #Local services
    if len(kwargs['local_tcp_ports']):
        tab = __sub(','.join(kwargs['local_tcp_ports']).split(','), 11)
        for a in tab:
            res += __execute('iptables -A INPUT-RIVNET -p tcp -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -j ACCEPT')


    if len(kwargs['local_udp_ports']):
        tab = __sub(','.join(kwargs['local_udp_ports']).split(','), 10)
        for a in tab:
            res += __execute('iptables -A INPUT-RIVNET -p udp -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -j ACCEPT')

    # ICMP : ping request
    res += __execute('iptables -A INPUT-RIVNET -p icmp -j ACCEPT')

    # Don't touch to the established connections !
    # 'state' module, obsolete but still used
    res += __execute('iptables -A INPUT-RIVNET -m state --state ESTABLISHED,RELATED -j ACCEPT')
    res += __execute('iptables -A FORWARD-RIVNET -m state --state ESTABLISHED,RELATED -j ACCEPT')
    # new module. 'conntrack' instead of 'state'
    res += __execute('iptables -A INPUT-RIVNET -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT')
    res += __execute('iptables -A OUTPUT -m conntrack --ctstate NEW,RELATED,ESTABLISHED -j ACCEPT')

    # Routing Aldebaran
    res += __execute('iptables -A FORWARD-RIVNET -i ' + kwargs['lan_admin_int'] + ' -j ACCEPT')

    # Routing Wan to Lan network
    res += __execute('iptables -A FORWARD-RIVNET -i ' + kwargs['wan_int'] + ' -j ACCEPT')
    res += __execute('iptables -A POSTROUTING-RIVNET -t nat -o ' + kwargs['lan_int'] + ' -j MASQUERADE')

    # Routing Wifi to Wan and Lan
    res += __execute('iptables -A FORWARD-RIVNET -i wlx00c0ca84a3dd -j ACCEPT')

    res += ["Clients: "]
    res += ["\n"]

    for client in kwargs['clients']:
        for mac in client["macs"]:

            name = client["name"]

            res += __execute('iptables -A FORWARD-RIVNET -i ' + kwargs['lan_int'] + ' -p icmp -m mac --mac-source ' + mac + ' -m comment --comment "' + name + '" -j ACCEPT')

            if client["admin"]:

                res += __execute('iptables -A FORWARD-RIVNET -i ' + kwargs['lan_int'] + ' -m mac --mac-source ' + mac + ' -m state --state NEW -m comment --comment "' + name + '" -j ACCEPT')

            else:

                if len(kwargs['forward_tcp_ports']):
                    tab = __sub(','.join(kwargs['forward_tcp_ports']).split(','), 10)
                    for a in tab:
                        res += __execute('iptables -A FORWARD-RIVNET -i ' + kwargs['lan_int'] + ' -o ' + kwargs['wan_int'] + '  -p tcp -m mac --mac-source ' + mac + ' -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -m comment --comment "' + name + '" -j ACCEPT')

                if len(kwargs['forward_udp_ports']):
                    tab = __sub(','.join(kwargs['forward_udp_ports']).split(','), 10)
                    for a in tab:
                        res += __execute('iptables -A FORWARD-RIVNET -i ' + kwargs['lan_int'] + ' -o ' + kwargs['wan_int'] + '  -p udp -m mac --mac-source ' + mac + ' -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -m comment --comment "' + name + '" -j ACCEPT')

    res += ["\n"]
    res += __execute('iptables -t nat -A POSTROUTING-RIVNET -j SNAT -o ' + kwargs['wan_int'] + ' --to-source ' + kwargs['wan_ip'])
    #res += __execute('iptables -t nat -A POSTROUTING-RIVNET -j MASQUERADE')

    res += __execute('bash firewall/save.sh')

    res += ["\n"]
    return { 'start_log': res }
 

def stop():
    res = []

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
    res += __execute('iptables  -F INPUT-RIVNET')
    res += __execute('iptables  -F OUTPUT-RIVNET')
    res += __execute('iptables  -F FORWARD-RIVNET')
    res += __execute('iptables  -t nat -F PREROUTING-RIVNET')
    res += __execute('iptables  -t nat -F POSTROUTING-RIVNET')

    return { 'stop_log': res }


def restart(kwargs):
    res = stop()
    res.update(start(kwargs))
    return res
