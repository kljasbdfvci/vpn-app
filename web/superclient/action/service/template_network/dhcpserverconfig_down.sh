#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -dP|--dnsmasq_pid_file)
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

# dhcpServerConfig
if pgrep -f 'dnsmasq'; then
    killall 'dnsmasq' &>/dev/null
    sleep 1
fi

rm $dnsmasq_pid_file
rm $dnsmasq_log_file
rm $dnsmasq_lease_file

if pgrep -f 'dhcpd'; then
    killall 'dhcpd' &>/dev/null
    sleep 1
fi

rm $dhcpd_config_file
rm $dhcpd_pid_file
rm $dhcpd_log_file
rm $dhcpd_lease_file

if pgrep -f 'named'; then
    killall 'named' &>/dev/null
    sleep 1
fi

rm $named_config_file

exit $exit_code
