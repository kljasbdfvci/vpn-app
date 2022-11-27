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
