#!/bin/bash

parse_options() {
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
            --timeout)
                timeout="$2"
                shift # past argument
                shift # past value
                ;;
            --try_count)
                try_count="$2"
                shift # past argument
                shift # past value
                ;;
            --config)
                config="$2"
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

exit_code=""

if [[ -f $pid_file ]]; then
    rm $pid_file
fi
if [[ -f $log_file ]]; then
    rm $log_file
fi

v2ray -config $config &>$log_file &
pid=$!
exit_code=$?
if [ "$exit_code" == 0 ]; then
    echo -n $pid > $pid_file
fi

exit $exit_code
