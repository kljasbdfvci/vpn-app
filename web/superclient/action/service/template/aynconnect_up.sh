#! /bin/bash

gateway=$1
username=$2
password=$3
timeout=$4
pid_file=$5

exit_code=""

tmpfile1=$(mktemp)
tmpfile2=$(mktemp)

$(timeout $timeout openssl s_client -connect $gateway </dev/null 2>/dev/null | openssl x509 -text > $tmpfile1)
res1=$?
$(timeout $timeout openssl s_client -showcerts -connect $gateway </dev/null 2>/dev/null | openssl x509 -outform PEM > $tmpfile2)
res2=$?
if [ $res1 == 0 ] && [ $res2 == 0 ]; then
    servercert=$(openssl x509 -in $tmpfile2 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64)
    servercert="pin-sha256:"$servercert
    timeout $timeout echo $password | openconnect --protocol=anyconnect --pid-file=$pid_file --background $gateway --user=$username --passwd-on-stdin --servercert $servercert
    exit_code=$?
else
    exit_code=10
fi

rm $tmpfile1
rm $tmpfile2

echo $exit_code

exit $exit_code
