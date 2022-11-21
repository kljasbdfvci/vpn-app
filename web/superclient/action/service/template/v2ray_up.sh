#!/bin/bash

pid_file=${1}
log_file=${2}
timeout=${3}
try=${4}

config=${5}

exit_code=""

rm $pid_file
rm $log_file

v2ray -config $config &>$log_file &
pid=$!
exit_code=$?
if [ "$exit_code" == 0 ]; then
    echo -n $pid > $pid_file
fi

exit $exit_code
