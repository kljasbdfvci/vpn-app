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
        --log)
            log="yes"
            shift # past argument
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

exit_code=0

if [ -f "$pid_file" ]; then
    pid=$(cat $pid_file | xargs)
    kill -2 $pid || kill -9 $pid
    rm $pid_file
fi

if [ -f "$log_file" ]; then
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

if [ -f "$dns_log" ]; then
    rm $dns_log
fi

if [ -n "$(ip link show | grep $vpn_interface)" ]; then
    ifconfig $vpn_interface down &>/dev/null
    ip link set $vpn_interface down &>/dev/null
    ip link delete $vpn_interface &>/dev/null
    ip=""
    reg="[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    if [[ $v2ray_outbounds_ip =~ $reg ]]; then
        ip=$v2ray_outbounds_ip
    else
        ip=$(dig +short $v2ray_outbounds_ip)
    fi
    ip route del $ip &>/dev/null
fi

list=$(sysctl -a | grep "\.rp_filter")
for item in $list
do
	if [[ "$item" == *"rp_filter"* ]]; then
		sysctl -w $item=2
	fi
done

# iptables reset
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# ip_forward 1
sysctl -w net.ipv4.ip_forward=1

# policy
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# router
iptables -t nat -A POSTROUTING -j MASQUERADE

exit $exit_code
