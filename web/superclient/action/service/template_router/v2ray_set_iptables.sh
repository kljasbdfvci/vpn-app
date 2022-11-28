#!/bin/bash

########################################################################
# Define various configuration parameters.
########################################################################

TUN_INTERFACE=${1}
INTERNET_GW=$(route -n | grep 'UG' | awk {'print $2'} | head -n 1 | tr -d '\n')
SOCKS_IP="127.0.0.1"
SOCKS_PORT=${2}
SOCKS_SERVER_IP=${3}
BADVPN_TUN2SOCKS_LOG=${4}
DNS_MODE=${5}
DNSServer=${6}
DNS_LOG=${7}

########################################################################
# start dns
########################################################################

if [ $DNS_MODE == "_4" ]; then
	if pgrep -f 'DNS2SOCKS'; then
		killall 'DNS2SOCKS' &>/dev/null
		sleep 1
	fi

	#
	DNS2SOCKS $SOCKS_IP:$SOCKS_PORT $DNSServer 127.0.0.1:5300 /l:$DNS_LOG &>/dev/null &

	# iptables
	iptables -t nat -A OUTPUT -p tcp --dport 53 -j REDIRECT --to-port 5300
	iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-port 5300
fi

########################################################################
# start tuntap
########################################################################

if [ -n "$(ip link show | grep $TUN_INTERFACE)" ]; then
    ifconfig tun0 down &>/dev/null
    ip link set tun0 down &>/dev/null
    ip link delete tun0 &>/dev/null
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

if pgrep -f 'badvpn-tun2socks'; then
    killall 'badvpn-tun2socks' &>/dev/null
	sleep 1
fi

badvpn-tun2socks --tundev $TUN_INTERFACE --netif-ipaddr 10.0.0.2 --netif-netmask 255.255.255.0 --socks-server-addr $SOCKS_IP:$SOCKS_PORT --loglevel 3 --socks5-udp &>$BADVPN_TUN2SOCKS_LOG &>/dev/null &

########################################################################
# start iptables
########################################################################

# policy
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# ip_forward 1
sysctl -w net.ipv4.ip_forward=1

# .rp_filter 2
list=$(sysctl -a | grep "\.rp_filter")
for item in $list
do
	if [[ "$item" == *"rp_filter"* ]]; then
		sysctl -w $item=2
	fi
done

exit 0
