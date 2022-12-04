#!/bin/bash

POSITIONAL_ARGS=()
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
        -c|--hostapd_config_file)
            hostapd_config_file="$2"
            shift # past argument
            shift # past value
            ;;
        -P|--hostapd_pid_file)
            hostapd_pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        -l|--hostapd_log_file)
            hostapd_log_file="$2"
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

echo -e $config > $hostapd_config_file

hostapd_res=1
if [[ $log == "yes" ]]; then
    hostapd -B $hostapd_config_file -P $hostapd_pid_file -t -d &> $hostapd_log_file
    hostapd_res=$?
else
    hostapd -B $hostapd_config_file -P $hostapd_pid_file -t -d &> /dev/null
    hostapd_res=$?
fi

if [[ $hostapd_res == 0 ]]; then
    exit_code=0
else
    exit_code=1
fi

exit $exit_code
