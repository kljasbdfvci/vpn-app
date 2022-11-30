#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --pid_file)
            pid_file="$2"
            shift # past argument
            shift # past value
            ;;
        --log_file)
            log_file="$2"
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

if [ -f "$pid_file" ]; then
    pid=$(cat $pid_file | xargs)
    kill -2 $pid || kill -9 $pid
    rm $pid_file
fi

if [ -f "$log_file" ]; then
    rm $log_file
fi

# iptables reset
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# ip_forward 1
sysctl -w net.ipv4.ip_forward=1

# policy
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# router
iptables -t nat -A POSTROUTING -j MASQUERADE

exit 0
