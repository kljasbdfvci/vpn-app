#!/bin/bash

config=${1}
pid_file=${2}

exit_code=""

v2ray -config $config &>/dev/null &
pid=$!
wait $!
exit_code=$?
if [ "$exit_code" == 0 ]; then
    echo -n $pid > $pid_file
fi

exit $exit_code
