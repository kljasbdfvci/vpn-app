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
        --named_config_file)
            named_config_file="$2"
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

if [ $dhcp_module == "dnsmasq" ]; then

    list_interface=(`echo $interface | sed 's/,/\n/g'`)
    list_ip_address=(`echo $ip_address | sed 's/,/\n/g'`)
    list_subnet_mask=(`echo $subnet_mask | sed 's/,/\n/g'`)
    list_dhcp_ip_address_from=(`echo $dhcp_ip_address_from | sed 's/,/\n/g'`)
    list_dhcp_ip_address_to=(`echo $dhcp_ip_address_to | sed 's/,/\n/g'`)

    dhcp_range=""
    for i in "${!list_interface[@]}"; do
        temp_interface=${list_interface[$i]}
        temp_ip_address=${list_ip_address[$i]}
        temp_subnet_mask=${list_subnet_mask[$i]}
        temp_dhcp_ip_address_from=${list_dhcp_ip_address_from[$i]}
        temp_dhcp_ip_address_to=${list_dhcp_ip_address_to[$i]}

        ifconfig $temp_interface $temp_ip_address netmask $temp_subnet_mask up

        dhcp_range=$dhcp_range"--dhcp-range=interface:$temp_interface,$temp_dhcp_ip_address_from,$temp_dhcp_ip_address_to,$temp_subnet_mask,24h "
    done  

    dnsmasq_res=1
    if [[ $log == "yes" ]]; then
        dnsmasq --dhcp-authoritative --no-negcache --strict-order --clear-on-reload --log-queries --log-dhcp \
        --bind-interfaces --except-interface=lo \
        --interface=$interface --listen-address=$ip_address $dhcp_range \
        --log-facility=$dnsmasq_log_file --pid-file=$dnsmasq_pid_file --dhcp-leasefile=$dnsmasq_lease_file
        dnsmasq_res=$?
    else
        dnsmasq --dhcp-authoritative --no-negcache --strict-order --clear-on-reload --log-queries --log-dhcp \
        --bind-interfaces --except-interface=lo \
        --interface=$interface --listen-address=$ip_address $dhcp_range \
        --pid-file=$dnsmasq_pid_file --dhcp-leasefile=$dnsmasq_lease_file &> /dev/null
        dnsmasq_res=$?
    fi

    if [[ $dnsmasq_res == 0 ]]; then
        exit_code=0
    else
        exit_code=1
    fi
    
elif [ $dhcp_module == "isc-dhcp-server" ]; then

    list_interface=(`echo $interface | sed 's/,/\n/g'`)
    list_ip_address=(`echo $ip_address | sed 's/,/\n/g'`)
    list_subnet_mask=(`echo $subnet_mask | sed 's/,/\n/g'`)
    list_dhcp_ip_address_from=(`echo $dhcp_ip_address_from | sed 's/,/\n/g'`)
    list_dhcp_ip_address_to=(`echo $dhcp_ip_address_to | sed 's/,/\n/g'`)

    str_interface=""

    cat > $dhcpd_config_file << EOF
authoritative;
EOF

    for i in "${!list_interface[@]}"; do
        temp_interface=${list_interface[$i]}
        temp_ip_address=${list_ip_address[$i]}
        temp_subnet_mask=${list_subnet_mask[$i]}
        temp_dhcp_ip_address_from=${list_dhcp_ip_address_from[$i]}
        temp_dhcp_ip_address_to=${list_dhcp_ip_address_to[$i]}

        ifconfig $temp_interface $temp_ip_address netmask $temp_subnet_mask up

        network_range=$(echo -n $temp_ip_address | sed 's/\([[:digit:]]\{1,3\}\(\.[[:digit:]]\{1,3\}\)\{2\}\.\)\([[:digit:]]\{1,3\}\)/\1/g')"0"
    
        cat >> $dhcpd_config_file << EOF
subnet $network_range netmask $temp_subnet_mask {
  range $temp_dhcp_ip_address_from $temp_dhcp_ip_address_to;
  option domain-name-servers $temp_ip_address;
  option routers $temp_ip_address;
  default-lease-time 86400;
  max-lease-time 86400;
}
EOF
    str_interface=$str_interface" "$temp_interface
    done

    touch $dhcpd_lease_file
    
    dhcpd_res=1
    if [[ $log == "yes" ]]; then
        dhcpd -cf $dhcpd_config_file -pf $dhcpd_pid_file -tf $dhcpd_log_file -lf $dhcpd_lease_file $str_interface
        dhcpd_res=$?
    else
        dhcpd -cf $dhcpd_config_file -pf $dhcpd_pid_file -lf $dhcpd_lease_file $str_interface &> /dev/null
        dhcpd_res=$?
    fi

    str=""
    for item in ${dns_server//,/ } ; do
        str=$str"        $item;"$'\n'
    done

    cat > $named_config_file << EOF
options {
    directory "/var/cache/bind";

    forwarders {
$str
    };

    allow-query { any; };
};
EOF

    named_res=1
    if [[ $log == "yes" ]]; then
        named -c $named_config_file
        named_res=$?
    else
        named -c $named_config_file &> /dev/null
        named_res=$?
    fi

    if [[ $dhcpd_res == 0 ]] && [[ $named_res == 0 ]]; then
        exit_code=0
    else
        exit_code=1
    fi

fi

exit $exit_code
