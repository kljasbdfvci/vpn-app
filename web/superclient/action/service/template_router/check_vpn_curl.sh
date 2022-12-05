#!/bin/bash

POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            domain="$2"
            shift # past argument
            shift # past value
            ;;
        --timeout)
            timeout="$2"
            shift # past argument
            shift # past value
            ;;
        --retry)
            retry="$2"
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

n=0
until [ "$n" -ge $retry ]
do
    echo "Try($n)"
    timeout $timeout curl $domain --connect-timeout $timeout --max-time $timeout
    exit_code=$?
    if [ $exit_code == 0 ]; then
        break
    fi
    n=$((n+1)) 
    sleep 1
done

exit $exit_code
