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
        --timeout)
            timeout="$2"
            shift # past argument
            shift # past value
            ;;
        --try_count)
            try_count="$2"
            shift # past argument
            shift # past value
            ;;
        --config)
            config="$2"
            shift # past argument
            shift # past value
            ;;
        --vpn_interface)
            vpn_interface="$2"
            shift # past argument
            shift # past value
            ;;
        --v2ray_inbounds_port)
            v2ray_inbounds_port="$2"
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
        --dns_mode)
            dns_mode="$2"
            shift # past argument
            shift # past value
            ;;
        --dns_server)
            dns_server="$2"
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

exit_code=1

if [ $log == "yes" ]; then
    v2ray -config $config &> $log_file &
    pid=$!
    exit_code=$?
elif
    v2ray -config $config &> /dev/null &
    pid=$!
    exit_code=$?
fi

if [ "$exit_code" == 0 ]; then

    ########################################################################
    # v2ray pid
    ########################################################################
    echo -n $pid > $pid_file

    ########################################################################
    # Define various configuration parameters.
    ########################################################################

    default_gateway=$(route -n | grep 'UG' | awk {'print $2'} | head -n 1 | tr -d '\n')
    v2ray_inbounds_ip="127.0.0.1"

    ########################################################################
    # start dns
    ########################################################################

    if [ -n "$dns_server" ] && [ -n "$dns_log" ]; then

        # DNS2SOCKS
        if [ $log == "yes" ]; then
            DNS2SOCKS $v2ray_inbounds_ip:$v2ray_inbounds_port $dns_server 127.0.0.1:5300 /l:$dns_log &> /dev/null &
        else
            DNS2SOCKS $v2ray_inbounds_ip:$v2ray_inbounds_port $dns_server 127.0.0.1:5300 &> /dev/null &
        fi

        # iptables
        iptables -t nat -A OUTPUT -p tcp --dport 53 -j REDIRECT --to-port 5300
        iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-port 5300
    fi

    ########################################################################
    # start tuntap
    ########################################################################

    ip tuntap add dev $vpn_interface mode tun
    ip addr add dev $vpn_interface 10.0.0.1/24
    ip link set dev $vpn_interface up

    route add -net 0.0.0.0 netmask 0.0.0.0 dev $vpn_interface
    ip route add $v2ray_outbounds_ip via $default_gateway

    sleep 1

    ########################################################################
    # start badvpn-tun2socks
    ########################################################################

    if [ $log == "yes" ]; then
        badvpn-tun2socks --tundev $vpn_interface --netif-ipaddr 10.0.0.2 --netif-netmask 255.255.255.0 --socks-server-addr \
        $v2ray_inbounds_ip:$v2ray_inbounds_port --loglevel 3 --socks5-udp &> $badvpn_tun2socks_log_file &> /dev/null &
    else
        badvpn-tun2socks --tundev $vpn_interface --netif-ipaddr 10.0.0.2 --netif-netmask 255.255.255.0 --socks-server-addr \
        $v2ray_inbounds_ip:$v2ray_inbounds_port --loglevel 3 --socks5-udp &> /dev/null &
    fi

    ########################################################################
    # start iptables
    ########################################################################
    
    # .rp_filter 2
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
fi

exit $exit_code
