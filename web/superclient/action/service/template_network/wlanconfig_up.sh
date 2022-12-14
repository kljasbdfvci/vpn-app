#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--interface)
            interface="$2"
            shift # past argument
            shift # past value
            ;;
        -s1|--ssid1)
            ssid1="$2"
            shift # past argument
            shift # past value
            ;;
        -p1|--wpa_passphrase1)
            wpa_passphrase1="$2"
            shift # past argument
            shift # past value
            ;;
        -s2|--ssid2)
            ssid2="$2"
            shift # past argument
            shift # past value
            ;;
        -p2|--wpa_passphrase2)
            wpa_passphrase2="$2"
            shift # past argument
            shift # past value
            ;;
        -s3|--ssid3)
            ssid3="$2"
            shift # past argument
            shift # past value
            ;;
        -p3|--wpa_passphrase3)
            wpa_passphrase3="$2"
            shift # past argument
            shift # past value
            ;;
        -s4|--ssid4)
            ssid4="$2"
            shift # past argument
            shift # past value
            ;;
        -p4|--wpa_passphrase4)
            wpa_passphrase4="$2"
            shift # past argument
            shift # past value
            ;;
        -cc|--country_code)
            country_code="$2"
            shift # past argument
            shift # past value
            ;;
        -D|--driver)
            driver="$2"
            shift # past argument
            shift # past value
            ;;
        -c|--wpa_supplicant_config_file)
            wpa_supplicant_config_file="$2"
            shift # past argument
            shift # past value
            ;;
        -P|--wpa_supplicant_pid_file)
            wpa_supplicant_pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        -f|--wpa_supplicant_log_file)
            wpa_supplicant_log_file="$2"
            shift # past argument
            shift # past value
            ;;
        -d|--dhcp)
            dhcp="yes"
            shift # past argument
            ;;
        -D|--dns_manage_up)
            dns_manage_up="$2"
            shift # past argument
            shift # past value
            ;;
        -ip1|--ip_address_1)
            ip_address_1="$2"
            shift # past argument
            shift # past value
            ;;
        -mask1|--subnet_mask_1)
            subnet_mask_1="$2"
            shift # past argument
            shift # past value
            ;;
        -ip2|--ip_address_2)
            ip_address_2="$2"
            shift # past argument
            shift # past value
            ;;
        -mask2|--subnet_mask_2)
            subnet_mask_2="$2"
            shift # past argument
            shift # past value
            ;;
        -ip3|--ip_address_3)
            ip_address_3="$2"
            shift # past argument
            shift # past value
            ;;
        -mask3|--subnet_mask_3)
            subnet_mask_1="$2"
            shift # past argument
            shift # past value
            ;;
        -ip4|--ip_address_4)
            ip_address_4="$2"
            shift # past argument
            shift # past value
            ;;
        -mask4|--subnet_mask_4)
            subnet_mask_1="$2"
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

cat > $wpa_supplicant_config_file << EOF
update_config=1
country=$country_code
EOF

if [[ -n $ssid1 ]] && [[ -n $wpa_passphrase1 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid1"
    proto=WPA2
    psk="$wpa_passphrase1"
    key_mgmt=WPA-PSK
    pairwise=CCMP TKIP
    group=CCMP TKIP
    priority=4
}
EOF
elif [[ -n $ssid1 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid1"
    key_mgmt=NONE
    priority=4
}
EOF
fi

if [[ -n $ssid2 ]] && [[ -n $wpa_passphrase2 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid2"
    proto=WPA2
    psk="$wpa_passphrase2"
    key_mgmt=WPA-PSK
    pairwise=CCMP TKIP
    group=CCMP TKIP
    priority=3
}
EOF
elif [[ -n $ssid2 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid2"
    key_mgmt=NONE
    priority=3
}
EOF
fi

if [[ -n $ssid3 ]] && [[ -n $wpa_passphrase3 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid3"
    proto=WPA2
    psk="$wpa_passphrase3"
    key_mgmt=WPA-PSK
    pairwise=CCMP TKIP
    group=CCMP TKIP
    priority=2
}
EOF
elif [[ -n $ssid3 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid3"
    key_mgmt=NONE
    priority=2
}
EOF
fi

if [[ -n $ssid4 ]] && [[ -n $wpa_passphrase4 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid4"
    proto=WPA2
    psk="$wpa_passphrase4"
    key_mgmt=WPA-PSK
    pairwise=CCMP TKIP
    group=CCMP TKIP
    priority=1
}
EOF
elif [[ -n $ssid4 ]]; then
    cat >> $wpa_supplicant_config_file << EOF
network={
    scan_ssid=1
    ssid="$ssid4"
    key_mgmt=NONE
    priority=1
}
EOF
fi

# wpa_supplicant
ifconfig $interface up
if [[ $log == "yes" ]]; then
    wpa_supplicant -B -D $driver -c $wpa_supplicant_config_file -P $wpa_supplicant_pid_file -i $interface -f $wpa_supplicant_log_file -t -dd
else
    wpa_supplicant -B -D $driver -c $wpa_supplicant_config_file -P $wpa_supplicant_pid_file -i $interface &> /dev/null
fi
sleep 10

# dhcp
dhcp_res=0
if [[ $dhcp == "yes" ]]; then
    ifconfig $interface up
    n=0
    try=2
    until [ "$n" -ge $try ]
    do
        echo "Try($n)"
        timeout 30 dhclient -v $interface
        dhcp_res=$?
        if [ $dhcp_res == 0 ]; then
            $dns_manage_up
            break
        fi
        n=$((n+1)) 
        sleep 1
    done
fi

# static 1
ip1_res=0
if [[ -n $ip_address_1 ]] && [[ -n $subnet_mask_1 ]]; then
    ifconfig $interface:1 $ip_address_1 netmask $subnet_mask_1 up
    ip1_res=$?
fi

# static 2
ip2_res=0
if [[ -n $ip_address_2 ]] && [[ -n $subnet_mask_2 ]]; then
    ifconfig $interface:2 $ip_address_2 netmask $subnet_mask_2 up
    ip2_res=$?
fi

# static 3
ip3_res=0
if [[ -n $ip_address_3 ]] && [[ -n $subnet_mask_3 ]]; then
    ifconfig $interface:3 $ip_address_3 netmask $subnet_mask_3 up
    ip3_res=$?
fi

# static 4
ip4_res=0
if [[ -n $ip_address_4 ]] && [[ -n $subnet_mask_4 ]]; then
    ifconfig $interface:4 $ip_address_4 netmask $subnet_mask_4 up
    ip4_res=$?
fi

if [[ $dhcp_res == 0 ]] && [[ $ip1_res == 0 ]] && [[ $ip2_res == 0 ]] && [[ $ip3_res == 0 ]] && [[ $ip4_res == 0 ]]; then
    exit_code=0
else
    exit_code=1
fi

exit $exit_code
