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
packages=("python3" "python3-dev" "python3-pip" "net-tools" "hostapd" "dnsmasq" "jq")
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
# get hardware info
hardware=""
if [ -f /sys/firmware/devicetree/base/model ]; then
    hardware=$(cat /sys/firmware/devicetree/base/model | tr -d ' ' | tr '[:upper:]' '[:lower:]')
fi
# get os info
os_distro=""
os_version=""
if [ -f /etc/os-release ]; then
    os_distro=$(. /etc/os-release; echo -n $ID)
    os_version=$(. /etc/os-release; echo -n $VERSION_CODENAME)
fi
res_cps=0
tmp_os_file_path="$this_dir_path/../os"
files=$(find $tmp_os_file_path -type f)
for tmp_os_file in $files
do

    tmp_os_file_parent=$(dirname $tmp_os_file)
    tmp_os_file_filename=$(basename $tmp_os_file)

    # check file for os
    reg=".+___.+___.+___.+"
    if [[ $tmp_os_file_filename =~ $reg ]]; then # sshd___orangepizero___debian___bullseye
        tmp_os_file_name=$(echo -n $tmp_os_file_filename | sed 's/\(.*\)___.*___.*___.*/\1/')
        tmp_os_file_hardware=$(echo -n $tmp_os_file_filename | sed 's/.*___\(.*\)___.*___.*/\1/')
        tmp_os_file_os_distro=$(echo -n $tmp_os_file_filename | sed 's/.*___.*___\(.*\)___.*/\1/')
        tmp_os_file_os_version=$(echo -n $tmp_os_file_filename | sed 's/.*___.*___.*___\(.*\)/\1/')
        if [[ "$hardware" == *"$tmp_os_file_hardware"* ]] && [[ "$os_distro" == "$tmp_os_file_os_distro" ]] && [[ "$os_version" == "$tmp_os_file_os_version" ]]; then
            os_file_parent=$(echo $tmp_os_file_parent | sed "s/^${tmp_os_file_path//\//\\\/}//")
            os_file_filename=$tmp_os_file_name
            os_file=$os_file_parent"/"$os_file_filename
        else
            continue
        fi
    else
        os_file_parent=$(echo $tmp_os_file_parent | sed "s/^${tmp_os_file_path//\//\\\/}//")
        os_file_filename=$tmp_os_file_filename
        os_file=$os_file_parent"/"$os_file_filename
    fi

    # get md5sum
    tmp_os_file_md5sum=$(md5sum $tmp_os_file | cut -d ' ' -f 1 | tr -d '\n')
    os_file_md5sum=""
    if [ -f "$os_file" ]; then
        os_file_md5sum=$(md5sum $os_file | cut -d ' ' -f 1 | tr -d '\n')
    fi
    
    if [ "$tmp_os_file_md5sum" != "$os_file_md5sum" ]; then
        flag_rebbot=1
        # do copy
        mkdir -p $os_file_parent && cp -f $tmp_os_file $os_file
        res_cp=$?
        if [ $res_cp -ne 0 ]; then
            res_cps=1
        fi
        # if systemd file change
        if [ "$os_file_parent" == "/lib/systemd/system" ]; then
            systemctl daemon-reload
            sleep 1
            systemctl enable $os_file_filename
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
python3 "$this_dir_path/../web/manage.py" runserver --noreload 1>/tmp/app-web.log 2>/tmp/app-web.log.error &

# if anychange in os reboot
if [ $flag_rebbot -eq 1 ]; then 
    echo "reboot successful."
    reboot
else
    echo "reboot not need."
fi
