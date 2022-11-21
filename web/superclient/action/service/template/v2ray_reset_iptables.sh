#!/bin/bash

sysctl -w net.ipv4.ip_forward=0

iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

if pgrep redsocks; then
    killall redsocks
    sleep 1
fi

if pgrep DNS2SOCKS; then
    killall DNS2SOCKS
    sleep 1
fi

if [ -n "$(ip rule show table 100)" ]; then
    ip rule  del   table 100 &>/dev/null
    ip route flush table 100 &>/dev/null
    sleep 1
fi

if pgrep badvpn-tun2socks; then
    killall badvpn-tun2socks
    sleep 1
fi

if [ -n "$(ip link show | grep tun0)" ]; then
    ifconfig tun0 down
    ip link set tun0 down
    ip link delete tun0
    sleep 1
fi

list=$(sysctl -a | grep "\.rp_filter")
for item in $list
do
	if [[ "$item" == *"rp_filter"* ]]; then
		sysctl -w $item=0
	fi
done

exit 0
