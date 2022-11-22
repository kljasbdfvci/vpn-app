#!/bin/bash

########################################################################
# Define various configuration parameters.
########################################################################

SUBNET_INTERFACE=${1}
TUN_INTERFACE=${2}
INTERNET_INTERFACE=${3}
INTERNET_GW=$(route -n | grep $INTERNET_INTERFACE | grep 'UG' | awk {'print $2'} | head -n 1 | tr -d '\n')
SOCKS_IP="127.0.0.1"
SOCKS_PORT=${4}
SOCKS_SERVER_IP=${5}
BADVPN_TUN2SOCKS_LOG=${6}
USE_DNS2SOCKS=${7}
DNSServer=${8}
DNS2SOCKS_LOG=${9}

########################################################################
# start dns2socks
########################################################################

if pgrep DNS2SOCKS; then
    killall DNS2SOCKS
    sleep 1
fi

if [[ "$USE_DNS2SOCKS" == "True" ]]; then
	#
	DNS2SOCKS $SOCKS_IP:$SOCKS_PORT $DNSServer 127.0.0.1:5300 /l:$DNS2SOCKS_LOG &>/dev/null &

	# iptables
	iptables -t nat -A OUTPUT -p tcp --dport 53 -j REDIRECT --to-port 5300
	iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-port 5300
fi

########################################################################
# start tuntap
########################################################################

if [ -n "$(ip link show | grep $TUN_INTERFACE)" ]; then
    ifconfig tun0 down
    ip link set tun0 down
    ip link delete tun0
	sleep 1
fi

ip tuntap add dev $TUN_INTERFACE mode tun
ip addr add dev $TUN_INTERFACE 10.0.0.1/24
ip link set dev $TUN_INTERFACE up

route add -net 0.0.0.0 netmask 0.0.0.0 dev $TUN_INTERFACE
ip route add $SOCKS_SERVER_IP via $INTERNET_GW

sleep 1

########################################################################
# start badvpn-tun2socks
########################################################################

if pgrep badvpn-tun2socks; then
    killall badvpn-tun2socks
	sleep 1
fi

badvpn-tun2socks --tundev $TUN_INTERFACE --netif-ipaddr 10.0.0.2 --netif-netmask 255.255.255.0 --socks-server-addr $SOCKS_IP:$SOCKS_PORT --loglevel 4 --socks5-udp &>$BADVPN_TUN2SOCKS_LOG &

########################################################################
# iptables
########################################################################


# ip_forward 1
sysctl -w net.ipv4.ip_forward=1

#
iptables -t nat -A POSTROUTING -j MASQUERADE

# .rp_filter 2
list=$(sysctl -a | grep "\.rp_filter")
for item in $list
do
	if [[ "$item" == *"rp_filter"* ]]; then
		sysctl -w $item=2
	fi
done

exit 0
