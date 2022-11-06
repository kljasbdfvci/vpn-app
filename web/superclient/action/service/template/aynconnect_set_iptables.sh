#!/bin/bash

SUBNET_INTERFACE=${1}
TUN_INTERFACE=${2}

sysctl -w net.ipv4.ip_forward=1

iptables -t nat -A POSTROUTING -o $TUN_INTERFACE -j MASQUERADE
iptables -A FORWARD -i $TUN_INTERFACE -o $SUBNET_INTERFACE -j ACCEPT -m state --state RELATED,ESTABLISHED
iptables -A FORWARD -i $SUBNET_INTERFACE -o $TUN_INTERFACE -j ACCEPT
iptables -A OUTPUT --out-interface $SUBNET_INTERFACE -j ACCEPT
iptables -A INPUT --in-interface $SUBNET_INTERFACE -j ACCEPT

exit 0
