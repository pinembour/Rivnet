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
    print("TEST ============")
    print("a: " + str(tab))
    for a in tab:
        print("b: " + a)
        print("c: " + a)
        temp.append(a)
        i += 1
        if i == size:
            print(temp)
            i = 0
            res.append(temp)
            temp = []
    if i > 0:
        res.append(temp)

    return res

def __init(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports):
    res = []
    res += __execute('echo 1 > /proc/sys/net/ipv4/ip_forward')
    res += __execute('echo 0 > /proc/sys/net/ipv6/conf/all/forwarding')

    res += __execute('iptables -P INPUT ACCEPT')
    res += __execute('iptables -P FORWARD ACCEPT')

    #res += __execute('iptables -N INVALID')

    res += __execute('iptables -A INPUT -i lo -j ACCEPT')

    res += __execute('iptables -A INPUT -p tcp -m multiport --dports 22,8000 -m state --state NEW -j ACCEPT')

    #Local services
    if local_tcp_ports:
        tab = __sub(','.join(local_tcp_ports).split(','), 11)
        for a in tab:
            res += __execute('iptables -A INPUT -p tcp -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -j ACCEPT')


    if local_udp_ports:
        tab = __sub(','.join(local_udp_ports).split(','), 10)
        for a in tab:
            res += __execute('iptables -A INPUT -p udp -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -j ACCEPT')

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
    #res += __execute('iptables -A POSTROUTING -t nat -s ' + lan_admin_int + ' -o ' + wan_int + ' -j MASQUERADE')

    # Routing Wan to Lan network
    res += __execute('iptables -A FORWARD -i ' + wan_int + ' -j ACCEPT')
    res += __execute('iptables -A POSTROUTING -t nat -o ' + lan_int + ' -j MASQUERADE')

    # Port forwarding rivlink's irc
    res += __execute('iptables -A PREROUTING -t nat -i ' + wan_int + ' -p tcp --dport 6667 -j DNAT --to 10.20.0.3:6667')
    res += __execute('iptables -A FORWARD -p tcp --dport 6667 -j ACCEPT')
    res += __execute('iptables -A PREROUTING -t nat -i ' + wan_int + ' -p tcp --dport 6668 -j DNAT --to 10.20.0.3:6668')
    res += __execute('iptables -A FORWARD -p tcp --dport 6668 -j ACCEPT')

    # VPN
    res += __execute('iptables -A INPUT -s 10.8.0.0/24 -j ACCEPT')
    res += __execute('iptables -A FORWARD -p tcp -s 10.8.0.0/24 -j ACCEPT')
    res += __execute('iptables -A POSTROUTING -t nat -s 10.8.0.0/24 -j MASQUERADE')
    res += __execute('iptables -A POSTROUTING -t nat -s 10.8.0.0/24 -j MASQUERADE')
    res += ["\n"]

    return res

def __route(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports, forward_tcp_ports, forward_udp_ports, clients):

    res = []
    res += ["Clients: "]
    res += ["\n"]

    for client in clients:
        for mac in client["macs"]:

            name = client["name"]

            res += __execute('iptables -A FORWARD -i ' + lan_int + ' -o ' + wan_int + '  -p icmp -m mac --mac-source ' + mac + ' -m comment --comment "' + name + '" -j ACCEPT')

            if client["admin"]:

                res += __execute('iptables -A FORWARD -i ' + lan_int + ' -o ' + wan_int + ' -m mac --mac-source ' + mac + ' -m state --state NEW -m comment --comment "' + name + '" -j ACCEPT')

            else:

                if forward_tcp_ports:
                    tab = __sub(','.join(forward_tcp_ports).split(','), 10)
                    for a in tab:
                        res += __execute('iptables -A FORWARD -i ' + lan_int + ' -o ' + wan_int + '  -p tcp -m mac --mac-source ' + mac + ' -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -m comment --comment "' + name + '" -j ACCEPT')

                if forward_udp_ports:
                    tab = __sub(','.join(forward_udp_ports).split(','), 10)
                    for a in tab:
                        res += __execute('iptables -A FORWARD -i ' + lan_int + ' -o ' + wan_int + '  -p udp -m mac --mac-source ' + mac + ' -m multiport --dports ' + ','.join(a) + ' -m state --state NEW -m comment --comment "' + name + '" -j ACCEPT')


    res += ["\n"]
    return res

def __finalize(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports):

    # NAT
    res = []
    res += ["\n"]
    res += __execute('iptables -t nat -A POSTROUTING -j SNAT -o ' + wan_int + ' --to-source ' + wan_ip)

    res += __execute('bash /opt/rivnet/save.sh')


    #res += __execute('iptables -A INVALID -j LOG --log-prefix "[===========================] "')
    #res += __execute('iptables -A INVALID -j DROP')

    return res

def start(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports, forward_tcp_ports, forward_udp_ports, clients):

    res = __init(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports)
    res += __route(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports, forward_tcp_ports, forward_udp_ports, clients)
    res += __finalize(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports)

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
    res += __execute('iptables  -F INPUT')
    res += __execute('iptables  -F OUTPUT')
    res += __execute('iptables  -F FORWARD')
    res += __execute('iptables  -t nat -F')

    # Delete chains
    #res += __execute('iptables  -F INVALID')
    #res += __execute('iptables  -X INVALID')

    return { 'stop_log': res }

def restart(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports, forward_tcp_ports, forward_udp_ports, clients):
    res = stop()
    res.update(start(wan_int, wan_ip, wan_r, lan_int, lan_ip, lan_r, lan_admin_int, lan_admin_ip, lan_admin_r, local_tcp_ports, local_udp_ports, forward_tcp_ports, forward_udp_ports, clients))
    return res
