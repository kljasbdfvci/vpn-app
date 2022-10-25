#!/bin/bash

this_file_path=$(eval "realpath $0")
this_dir_path=$(eval "dirname $this_file_path")

# install list of apt packages
packages=("python3-pip")
for package in ${packages[@]}
do
    if [ -z "$(dpkg -l | grep $package)" ]
    then
        apt install -y $package
        echo "$package is installed."
    else
        echo "$package is exist."
    fi
done

### reboot
flag_rebbot=0

### copy tmp os files to os
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
        # if process is running
        if pgrep -x $filename > /dev/null
        then
            pgrep $filename | xargs kill
            sleep 1
        fi
        # do copy
        mkdir -p $parent && cp $tmp_os_file $os_file
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
    fi

done
if [ $res_cps -eq 0 ]; then
    echo "copy os files successful."
else
    echo "copy os files failed."
fi

#

# if anychange in os reboot
if [ $flag_rebbot -eq 1 ]; then
    echo "reboot successful."
    reboot
fi
