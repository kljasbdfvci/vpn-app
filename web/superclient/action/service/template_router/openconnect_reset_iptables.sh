#!/bin/bash

parse_options() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -*|--*)
                echo "Unknown option $1"
                exit 1
                ;;
            *)
                echo "Invalid value $1"
                exit 1
                ;;
        esac
    done
}

parse_options $@

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

exit 0
