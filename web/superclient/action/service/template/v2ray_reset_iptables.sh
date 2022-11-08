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
fi

if pgrep DNS2SOCKS; then
    killall DNS2SOCKS
fi

exit 0
