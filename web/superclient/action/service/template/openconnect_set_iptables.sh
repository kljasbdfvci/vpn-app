#!/bin/bash

SUBNET_INTERFACE=${1}
TUN_INTERFACE=${2}
DNS_MODE=${3}
DNSServer=${4}
DNS_LOG=${5}

########################################################################
# start dns
########################################################################

if [ $DNS_MODE == "_2" ]; then

	# remove old dns
	if [ -n "$(cat /etc/resolv.conf | grep '#MYDNS_')" ]; then
		sed -n -e '/#MYDNS_START/,/#MYDNS_END/!p' -i /etc/resolv.conf
		sleep 1
	fi

	# make dns str
	str="#MYDNS_START\n"
	for item in ${DNSServer//,/ } ; do
		str=$str"nameserver $item\n"
	done
	str=$str"#MYDNS_END"

	# add new dns
	echo -e "$str\n$(cat /etc/resolv.conf)" > /etc/resolv.conf
    
fi

########################################################################
# start iptables
########################################################################

# policy
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# ip_forward 1
sysctl -w net.ipv4.ip_forward=1

#
iptables -t nat -A POSTROUTING -j MASQUERADE

exit 0
