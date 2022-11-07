#!/bin/bash

pid_file=${1}
log_file=${2}
timeout=${3}
try=${4}

config=${5}

exit_code=""

v2ray -config $config &>$log_file &
pid=$!
exit_code=$?
if [ "$exit_code" == 0 ]; then
    echo -n $pid > $pid_file
fi

exit $exit_code
