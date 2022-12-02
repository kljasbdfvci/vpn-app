#!/bin/bash

this_file_path=$(eval "realpath $0")
this_dir_path=$(eval "dirname $this_file_path")

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

# lanConfig
for dev in $($this_dir_path/interface_list.sh eth); do
    ifconfig $dev down
    ifconfig $dev:1 down
    ifconfig $dev:2 down
    ifconfig $dev:3 down
    ifconfig $dev:4 down
    sleep 1
done

exit $exit_code
