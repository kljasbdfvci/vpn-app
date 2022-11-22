#!/bin/bash

SUBNET_INTERFACE=${1}
TUN_INTERFACE=${2}

# policy
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# ip_forward 1
sysctl -w net.ipv4.ip_forward=1

#
iptables -t nat -A POSTROUTING -j MASQUERADE

exit 0
