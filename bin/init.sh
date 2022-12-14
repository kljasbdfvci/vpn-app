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
    if [[ -f /var/lib/dpkg/lock-frontend ]]; then
        rm /var/lib/dpkg/lock-frontend
    fi
    if [[ -f /var/lib/dpkg/lock ]]; then
        rm /var/lib/dpkg/lock
    fi
    echo "start apt update"
    DEBIAN_FRONTEND=noninteractive apt update --fix-missing
    res_update=$?
    sleep 1
    echo "start apt upgrade"
    DEBIAN_FRONTEND=noninteractive apt-get upgrade --fix-broken --fix-missing --assume-yes -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"
    res_upgrade=$?
    sleep 1
    if [[ $res_update == 0 ]] && [[ $res_upgrade == 0 ]]; then
        echo -n $now_time > $last_update_time_path
        echo "system update successful."
    else
        echo "system update failed."
    fi
else
    echo "system update not need."
fi

# install list of apt packages
packages=("avahi-daemon" "avahi-utils" "net-tools" "jq" "openssl" "python3" "python3-dev" "python3-pip" "sqlite3" "hostapd" "dnsmasq" "isc-dhcp-server" "bind9" "openconnect")
for package in ${packages[@]}
do
    if [ -z "$(dpkg -l | grep -w $package)" ]
    then
        n=0
        until [ "$n" -ge 3 ]
        do
            apt install -y $package
            res_apt=$?
            if [ $res_apt == 0 ]; then
                echo "try($n) $package is installed."
                break
            else
                echo "try($n) $package is install failed."
            fi
            n=$((n+1)) 
            sleep 1
        done
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
# get os arch
machine=$(uname -m)
res_cps=0
tmp_os_file_path="$this_dir_path/../os"
if [[ ! -d $tmp_os_file_path ]]; then
    tmp_os_file_path="/tmp/os"
fi
files=$(find $tmp_os_file_path -xtype f)
for tmp_os_file in $files
do

    tmp_os_file_parent=$(dirname $tmp_os_file)
    tmp_os_file_filename=$(basename $tmp_os_file)

    # check file for os
    reg=".*___.*___.*___.*___.*"
    if [[ $tmp_os_file_filename =~ $reg ]]; then # sshd___orangepizero___debian___bullseye___aarch64
        tmp_os_file_name=$(echo -n $tmp_os_file_filename | sed 's/\(.*\)___.*___.*___.*___.*/\1/')
        tmp_os_file_hardware=$(echo -n $tmp_os_file_filename | sed 's/.*___\(.*\)___.*___.*___.*/\1/')
        tmp_os_file_os_distro=$(echo -n $tmp_os_file_filename | sed 's/.*___.*___\(.*\)___.*___.*/\1/')
        tmp_os_file_os_version=$(echo -n $tmp_os_file_filename | sed 's/.*___.*___.*___\(.*\)___.*/\1/')
        tmp_os_file_machine=$(echo -n $tmp_os_file_filename | sed 's/.*___.*___.*___.*___\(.*\)/\1/')
        if [[ "$hardware" == *"$tmp_os_file_hardware"* ]] && [[ "$os_distro" == "$tmp_os_file_os_distro" ]] && [[ "$os_version" == "$tmp_os_file_os_version" ]] && [[ "$machine" == "$tmp_os_file_machine" ]]; then
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
# delete os dir
rm -r $tmp_os_file_path
echo "delete os dir successful."
if [ $res_cps -eq 0 ]; then
    echo "copy os files successful."
else
    echo "copy os files failed."
fi

# disable hostapd
service="hostapd.service"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# disable dnsmasq
service="dnsmasq.service"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# disable isc-dhcp-server
service="isc-dhcp-server"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# disable named.service
service="named.service"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# disable redsocks.service
service="redsocks.service"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# disable serial-getty@ttyS0.service
service="serial-getty@ttyS0.service"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# disable serial-getty@ttyGS0.service
service="serial-getty@ttyGS0.service"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# disable getty@tty1.service
service="getty@tty1.service"
if [[ "$(systemctl is-enabled $service &>/dev/null ; echo $?)" == 0 ]]; then
    systemctl stop $service
    systemctl disable $service
    echo "$service is disabled."
else
    echo "$service is already disable."
fi

# kill pid if get port 80
port="80"
if [ -n "$(fuser $port/tcp)" ]; then
    fuser -k $port/tcp
    sleep 1
fi
if [ -n "$(fuser $port/udp)" ]; then
    fuser -k $port/udp
    sleep 1
fi

# pip
python3 -m pip install -r "$this_dir_path/../web/requirments.txt"

# if anychange in os reboot
if [ $flag_rebbot -eq 1 ]; then 
    echo "reboot successful."
    reboot
else
    echo "reboot not need."
fi

# clear history
rm /root/.bash_history
rm /home/*/.bash_history

# web
python3 "$this_dir_path/../web/manage.py" migrate
python3 "$this_dir_path/../web/manage.py" ensure_adminuser --username=admin --password=admin
ensure_general_path="/disk/ensure_general"
if [[ ! -f $ensure_general_path ]]; then
    python3 "$this_dir_path/../web/manage.py" ensure_general
    touch $ensure_general_path
    echo "create $ensure_general_path successful."
fi
ensure_lan_path="/disk/ensure_lan"
if [[ ! -f $ensure_lan_path ]]; then
    python3 "$this_dir_path/../web/manage.py" ensure_lan
    touch $ensure_lan_path
    echo "create $ensure_lan_path successful."
fi
ensure_hotspot_path="/disk/ensure_hotspot"
if [[ ! -f $ensure_hotspot_path ]]; then
    python3 "$this_dir_path/../web/manage.py" ensure_hotspot
    touch $ensure_hotspot_path
    echo "create $ensure_hotspot_path successful."
fi
ensure_dhcpserver_path="/disk/ensure_dhcpserver"
if [[ ! -f $ensure_dhcpserver_path ]]; then
    python3 "$this_dir_path/../web/manage.py" ensure_dhcpserver
    touch $ensure_dhcpserver_path
    echo "create $ensure_dhcpserver_path successful."
fi
python3 "$this_dir_path/../web/manage.py" network_apply
python3 "$this_dir_path/../web/manage.py" runserver 0.0.0.0:80 --noreload &>/tmp/app-web.log &
