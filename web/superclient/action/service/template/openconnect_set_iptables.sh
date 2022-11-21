#!/bin/bash

SUBNET_INTERFACE=${1}
TUN_INTERFACE=${2}

sysctl -w net.ipv4.ip_forward=1

iptables -A POSTROUTING -t nat -j MASQUERADE

exit 0
