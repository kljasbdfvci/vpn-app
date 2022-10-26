#!/bin/bash

this_file_path=$(eval "realpath $0")
this_dir_path=$(eval "dirname $this_file_path")

# make dir disk path
disk_path="/disk"
if [[ ! -d $disk_path ]]; then
    mkdir -p $disk_path
    echo "$disk_path create successful."
else
    echo "$disk_path exist."
fi

# update
last_update_time_path="$disk_path/update.sec"
last_update_time=0
if [ -f "$last_update_time_path" ]; then
    last_update_time=$(cat $last_update_time_path | tr -d '\n')
fi
now_time=$(date +%s)
if [[ "$now_time - $last_update_time" -gt 604800 ]]; then
    if [[ ! -f /var/lib/dpkg/lock-frontend ]]; then
        rm /var/lib/dpkg/lock-frontend
    fi
    if [[ ! -f /var/lib/dpkg/lock ]]; then
        rm /var/lib/dpkg/lock
    fi
    echo "start apt update"
    apt update --fix-missing
    sleep 1
    echo "start apt upgrade"
    apt upgrade --fix-broken --fix-missing -y
    sleep 1
    echo "start apt autoremove"
    apt autoremove -y
    sleep 1
    echo "start apt autoclean"
    apt autoclean -y
    sleep 1
    echo -n $now_time > $last_update_time_path
    echo "system update successful."
else
    echo "system update not need."
fi

# install list of apt packages
packages=("python3" "python3-dev" "python3-pip" "ifconfig" "hostapd" "dnsmasq")
for package in ${packages[@]}
do
    if [ -z "$(dpkg -l | grep $package)" ]
    then
        apt install -y $package
        sleep 1
        echo "$package is installed."
    else
        echo "$package is exist."
    fi
done

# reboot
flag_rebbot=0

# copy tmp os files to os
res_cps=0
tmp_os_file_path="$this_dir_path/../os"
files=$(find $tmp_os_file_path -type f)
for tmp_os_file in $files
do

    os_file=$(echo $tmp_os_file | sed "s/^${tmp_os_file_path//\//\\\/}//")
    tmp_os_file_md5sum=$(md5sum $tmp_os_file | cut -d ' ' -f 1 | tr -d '\n')
    os_file_md5sum=""
    if [ -f "$os_file" ]; then
        os_file_md5sum=$(md5sum $os_file | cut -d ' ' -f 1 | tr -d '\n')
    fi
    if [ "$tmp_os_file_md5sum" != "$os_file_md5sum" ]; then
        flag_rebbot=1
        parent=$(dirname $os_file)
        filename=$(basename $os_file)
        # do copy
        mkdir -p $parent && cp -f $tmp_os_file $os_file
        res_cp=$?
        if [ $res_cp -ne 0 ]; then
            res_cps=1
        fi
        # if systemd file change
        if [ "$parent" == "/lib/systemd/system" ]; then
            systemctl daemon-reload
            sleep 1
            systemctl enable $filename
        fi
        echo "copy file from $tmp_os_file to $os_file successful."
    fi

done
if [ $res_cps -eq 0 ]; then
    echo "copy os files successful."
else
    echo "copy os files failed."
fi

# web
python3 -m pip install -r "$this_dir_path/../web/requirments.txt"
python3 "$this_dir_path/../web/manage.py" migrate
python3 "$this_dir_path/../web/manage.py" ensure_adminuser --username=admin --password=admin
python3 "$this_dir_path/../web/manage.py" runserver 0.0.0.0:80 1>/tmp/app-web.log 2>/tmp/app-web.log.error &

# if anychange in os reboot
if [ $flag_rebbot -eq 1 ]; then 
    echo "reboot successful."
    reboot
else
    echo "reboot not need."
fi
