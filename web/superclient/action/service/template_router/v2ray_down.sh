#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --pid_file)
            pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        --log_file)
            log_file="$2"
            shift # past argument
            shift # past value
            ;;
        --vpn_interface)
            vpn_interface="$2"
            shift # past argument
            shift # past value
            ;;
        --v2ray_outbounds_ip)
            v2ray_outbounds_ip="$2"
            shift # past argument
            shift # past value
            ;;
        --badvpn_tun2socks_log_file)
            badvpn_tun2socks_log_file="$2"
            shift # past argument
            shift # past value
            ;;
        --dns_log)
            dns_log="$2"
            shift # past argument
            shift # past value
            ;;
        -*|--*)
            echo "Unknown option $1"
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1") # save positional arg
            shift # past argument
            ;;
    esac
done
set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

if [ -f $pid_file ]; then
    pid=$(cat $pid_file | xargs)
    kill -2 $pid || kill -9 $pid
    rm $pid_file
fi

if [ -f $log_file ]; then
    rm $log_file
fi

if pgrep -f 'badvpn-tun2socks'; then
    killall 'badvpn-tun2socks' &>/dev/null
fi

if [ -f $badvpn_tun2socks_log_file ]; then
    rm $badvpn_tun2socks_log_file
fi

if pgrep -f 'DNS2SOCKS'; then
    killall 'DNS2SOCKS' &>/dev/null
fi

if [ -f $dns_log ]; then
    rm $dns_log
fi

if [ -n "$(ip link show | grep $vpn_interface)" ]; then
    ifconfig $vpn_interface down &>/dev/null
    ip link set $vpn_interface down &>/dev/null
    ip link delete $vpn_interface &>/dev/null
    ip route del $v2ray_outbounds_ip &>/dev/null
fi

list=$(sysctl -a | grep "\.rp_filter")
for item in $list
do
	if [[ "$item" == *"rp_filter"* ]]; then
		sysctl -w $item=0
	fi
done

iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -Fsss
iptables -t mangle -X

sysctl -w net.ipv4.ip_forward=1

iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

exit 0
