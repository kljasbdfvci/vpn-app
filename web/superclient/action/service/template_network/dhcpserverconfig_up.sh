#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--interface)
            interface="$2"
            shift # past argument
            shift # past value
            ;;
        -ip|--ip_address)
            ip_address="$2"
            shift # past argument
            shift # past value
            ;;
        -mask|--subnet_mask)
            subnet_mask="$2"
            shift # past argument
            shift # past value
            ;;
        -from|--dhcp_ip_address_from)
            dhcp_ip_address_from="$2"
            shift # past argument
            shift # past value
            ;;
        -to|--dhcp_ip_address_to)
            dhcp_ip_address_to="$2"
            shift # past argument
            shift # past value
            ;;
        -d|--dns_server)
            dns_server="$2"
            shift # past argument
            shift # past value
            ;;
        -P|--dnsmasq_pid_file)
            dnsmasq_pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        -8|--dnsmasq_log_file)
            dnsmasq_log_file="$2"
            shift # past argument
            shift # past value
            ;;
        -l|--dnsmasq_lease_file)
            dnsmasq_lease_file="$2"
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

exit_code=0

address=""
if [ -n "$dns_server" ]; then
    address="--address="$dns
fi

ifconfig $interface $ip_address netmask $subnet_mask up
ip_res=$?

dnsmasq --dhcp-authoritative --no-negcache --strict-order --clear-on-reload --log-queries --log-dhcp \
--bind-interfaces --except-interface=lo \
--interface=$interface --listen-address=$ip_address --dhcp-range=interface:$interface,$dhcp_ip_address_from,$dhcp_ip_address_to,$subnet_mask,24h \
--log-facility=$dnsmasq_log_file --pid-file=$dnsmasq_pid_file --dhcp-leasefile=$dnsmasq_lease_file $address
dnsmasq_res=$?

if [[ $ip_res == 0 ]] && [[ $dnsmasq_res == 0 ]]; then
    exit_code=0
else
    exit_code=1
fi

exit $exit_code
