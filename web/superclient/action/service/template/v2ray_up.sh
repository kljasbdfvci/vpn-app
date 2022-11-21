#!/bin/bash

pid_file=${1}
log_file=${2}
timeout=${3}
try=${4}

config=${5}

exit_code=""

if [[ -f $pid_file ]]; then
    rm $pid_file
fi
if [[ -f $log_file ]]; then
    rm $log_file
fi

v2ray -config $config | rotatelogs -n 1 $log_file 1M &>/dev/null &
pid=$!
exit_code=$?
if [ "$exit_code" == 0 ]; then
    echo -n $pid > $pid_file
fi

exit $exit_code
