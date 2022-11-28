#!/bin/bash

exit_code=0

# lanConfig
for interface in $(ifconfig | cut -d ' ' -f1 | tr ':' '\n' | awk NF | grep 'eth')
do
    ifconfig $iface down
    ifconfig $iface:1 down
    ifconfig $iface:2 down
    ifconfig $iface:3 down
    ifconfig $iface:4 down
    sleep 1
done

# wlanConfig
nmcli radio wifi off
rfkill unblock wlan
if pgrep -f 'wpa_supplicant'; then
    killall 'wpa_supplicant' &>/dev/null
    sleep 1
fi

for interface in $(ifconfig | cut -d ' ' -f1 | tr ':' '\n' | awk NF | grep 'wl')
do
    ifconfig $iface down
    ifconfig $iface:1 down
    ifconfig $iface:2 down
    ifconfig $iface:3 down
    ifconfig $iface:4 down
    sleep 1
done

# hotspotConfig
if pgrep -f 'hostapd'; then
    killall 'hostapd' &>/dev/null
    sleep 1
fi

# dhcpServerConfig
if pgrep -f 'hostapd'; then
    killall 'hostapd' &>/dev/null
    sleep 1
fi

# dns
# remove old dns
if [ -n "$(cat /etc/resolv.conf | grep '#MYDNS_')" ]; then
    sed -n -e '/#MYDNS_START/,/#MYDNS_END/!p' -i /etc/resolv.conf
    sleep 1
fi

exit $exit_code
