#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
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

# dns
if [ -n "$(cat /etc/resolv.conf | grep '#MYDNS_')" ]; then
    sed -n -e '/#MYDNS_START/,/#MYDNS_END/!p' -i /etc/resolv.conf
    sleep 1
fi

exit $exit_code
