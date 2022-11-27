#!/bin/bash

parse_options() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -i|--interface)
                interface="$2"
                shift # past argument
                shift # past value
                ;;
            -c|--channel)
                channel="$2"
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
            -c|--hotspot_config_file)
                hotspot_config_file="$2"
                shift # past argument
                shift # past value
                ;;
            -P|--hotspot_pid_file)
                wpa_passphrase="$2"
                shift # past argument
                shift # past value
                ;;
            -l|--hotspot_log_file)
                hotspot_log_file="$2"
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

config=""
config=$config"interface=$interface\n"
config=$config"channel=$channel\n"
config=$config"ssid=$ssid\n"
config=$config"wpa_passphrase=$wpa_passphrase\n"
config=$config"driver=nl80211\n"
config=$config"hw_mode=g\n"
config=$config"macaddr_acl=0\n"
config=$config"auth_algs=1\n"
config=$config"ignore_broadcast_ssid=0\n"
config=$config"wpa=2\n"
config=$config"wpa_key_mgmt=WPA-PSK\n"
config=$config"wpa_pairwise=TKIP\n"
config=$config"rsn_pairwise=CCMP\n"

echo -e $config > $hotspot_config_file

hostapd -B $hotspot_config_file -P $hotspot_pid_file -t -d &> $hotspot_log_file
