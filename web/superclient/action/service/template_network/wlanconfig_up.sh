#!/bin/bash

parse_options() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--interface)
                interface="$2"
                shift # past argument
                shift # past value
                ;;
            -s|--ssid)
                ssid="$2"
                shift # past argument
                shift # past value
                ;;
            -p|--wpa_passphrase)
                wpa_passphrase="$2"
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
            -*|--*)
                echo "Unknown option $1"
                exit 1
                ;;
            *)
                echo "Invalid value $1"
                exit 1
                ;;
        esac
    done
}

parse_options $@

exit_code=0

# wpa_passphrase
wpa_passphrase "$ssid" "$wpa_passphrase" | tee $wpa_supplicant_config_file

# wpa_supplicant

wpa_supplicant -B -c $wpa_supplicant_config_file -P $wpa_supplicant_pid_file -f $wpa_supplicant_log_file -i $interface
sleep 5

# dhcp
dhcp_res=0
if [ $dhcp == "yes" ]; then
    timeout 30 dhclient -v $interface
    dhcp_res=$?
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
