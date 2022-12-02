#!/bin/bash

this_file_path=$(eval "realpath $0")
this_dir_path=$(eval "dirname $this_file_path")

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -wc|--wpa_supplicant_config_file)
            wpa_supplicant_config_file="$2"
            shift # past argument
            shift # past value
            ;;
        -wP|--wpa_supplicant_pid_file)
            wpa_supplicant_pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        -wl|--wpa_supplicant_log_file)
            wpa_supplicant_log_file="$2"
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

# wlanConfig
nmcli radio wifi off
rfkill unblock wlan

if pgrep -f 'wpa_supplicant'; then
    killall 'wpa_supplicant' &>/dev/null
    sleep 1
fi

rm $wpa_supplicant_config_file
rm $wpa_supplicant_pid_file
rm $wpa_supplicant_log_file

for dev in $($this_dir_path/interface_list.sh wlan); do
    ifconfig $dev down
    ifconfig $dev:1 down
    ifconfig $dev:2 down
    ifconfig $dev:3 down
    ifconfig $dev:4 down
    sleep 1
done

exit $exit_code
