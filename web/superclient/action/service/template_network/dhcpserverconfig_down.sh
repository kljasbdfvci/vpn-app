#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        -dP|--dnsmasq_pid_file)
            dnsmasq_pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        -d8|--dnsmasq_log_file)
            dnsmasq_log_file="$2"
            shift # past argument
            shift # past value
            ;;
        -dl|--dnsmasq_lease_file)
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

# dhcpServerConfig
if pgrep -f 'dnsmasq'; then
    killall 'dnsmasq' &>/dev/null
    sleep 1
fi

rm $dnsmasq_pid_file
rm $dnsmasq_log_file
rm $dnsmasq_lease_file

exit $exit_code
