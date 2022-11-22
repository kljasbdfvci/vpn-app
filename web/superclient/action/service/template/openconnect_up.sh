#!/bin/bash

pid_file=${1}
log_file=${2}
timeout=${3}
try=${4}

protocol=${5}
gateway=${6}
username=${7}
password=${8}
interface=${9}
no_dtls=${10}
if [ "$no_dtls" == "True" ]; then
    no_dtls="--no-dtls"
else
    no_dtls=""
fi
passtos=${11}
if [ "$passtos" == "True" ]; then
    passtos="--passtos"
else
    passtos=""
fi
no_deflate=${12}
if [ "$no_deflate" == "True" ]; then
    no_deflate="--no-deflate"
else
    no_deflate=""
fi
deflate=${13}
if [ "$deflate" == "True" ]; then
    deflate="--deflate"
else
    deflate=""
fi
no_http_keepalive=${14}
if [ "$no_http_keepalive" == "True" ]; then
    no_http_keepalive="--no-http-keepalive"
else
    no_http_keepalive=""
fi

exit_code=""

tmpfile1=$(mktemp)
tmpfile2=$(mktemp)
trap 'rm -f $tmpfile1 $tmpfile2' EXIT

if [[ -f $pid_file ]]; then
    rm $pid_file
fi
if [[ -f $log_file ]]; then
    rm $log_file
fi

#$(openssl s_client -connect $gateway </dev/null 2>/dev/null | openssl x509 -text > $tmpfile1)
#res1=$?
res1=0
$(openssl s_client -showcerts -connect $gateway </dev/null 2>/dev/null | openssl x509 -outform PEM > $tmpfile2)
res2=$?
if [ $res1 == 0 ] && [ $res2 == 0 ]; then
    servercert=$(openssl x509 -in $tmpfile2 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64)
    servercert="pin-sha256:"$servercert
    n=0
    until [ "$n" -ge $try ]
    do
        echo -e "\n\nTry($n)\n\n"
        timeout $timeout echo $password | \
        openconnect --reconnect-timeout=30 --background --passwd-on-stdin \
        $no_dtls $passtos $no_deflate $deflate $no_http_keepalive \
        --protocol=$protocol --interface=$interface --pid-file=$pid_file  $gateway --user=$username  --servercert $servercert &>$log_file
        exit_code=$?
        if [ $exit_code == 0 ]; then
            break
        fi
        n=$((n+1)) 
        sleep 1
    done
else
    exit_code=10
fi

exit $exit_code
