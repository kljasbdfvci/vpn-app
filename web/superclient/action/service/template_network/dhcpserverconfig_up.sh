#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--dhcp_module)
            dhcp_module="$2"
            shift # past argument
            shift # past value
            ;;
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
        --dnsmasq_pid_file)
            dnsmasq_pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        --dnsmasq_log_file)
            dnsmasq_log_file="$2"
            shift # past argument
            shift # past value
            ;;
        --dnsmasq_lease_file)
            dnsmasq_lease_file="$2"
            shift # past argument
            shift # past value
            ;;
        --interface_dhcpd)
            interface_dhcpd="$2"
            shift # past argument
            shift # past value
            ;;
        --dhcpd_config_file)
            dhcpd_config_file="$2"
            shift # past argument
            shift # past value
            ;;
        --dhcpd_pid_file)
            dhcpd_pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        --dhcpd_log_file)
            dhcpd_log_file="$2"
            shift # past argument
            shift # past value
            ;;
        --dhcpd_lease_file)
            dhcpd_lease_file="$2"
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

if [ $dhcp_module == "dnsmasq" ]; then
    address=""
    #if [ -n "$dns_server" ]; then
    #    address="--address="$dns
    #fi

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

    
elif [ $dhcp_module == "isc-dhcp-server" ]; then

    dhcpd -cf $dhcpd_config_file -pf $dhcpd_pid_file -tf $dhcpd_log_file -lf $dhcpd_lease_file $interface_dhcpd

    str=""
    for item in ${dns_server//,/ } ; do
        str=$str"        $item;\n"
    done

    cat > $dhcpd_config_file << EOF
options {
    directory "/var/cache/bind";

    forwarders {
        $str
    };

    allow-query { any; };
};
EOF

fi

exit $exit_code
