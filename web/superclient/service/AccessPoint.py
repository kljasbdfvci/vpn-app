from ast import ImportFrom
import logging
import shutil
import psutil
import time

from .ConfigItem import *
from .Execte import *

class AccessPoint:
    def __init__(self, interface, ssid, wpa_passphrase, ip, dhcp_ip_from, dhcp_ip_to, netmask):
        # hostapd configs
        self.interface = ConfigItem("interface", interface)
        self.ssid = ConfigItem("ssid", ssid)
        self.wpa_passphrase = ConfigItem("wpa_passphrase", wpa_passphrase)
        self.driver = ConfigItem("driver", "nl80211")
        self.hw_mode = ConfigItem("hw_mode", "g")
        self.channel = ConfigItem("channel", "6")
        self.macaddr_acl = ConfigItem("macaddr_acl", "0")
        self.auth_algs = ConfigItem("auth_algs", "1")
        self.ignore_broadcast_ssid = ConfigItem("ignore_broadcast_ssid", "0")
        self.wpa = ConfigItem("wpa", "2")
        self.wpa_key_mgmt = ConfigItem("wpa_key_mgmt", "WPA-PSK")
        self.wpa_pairwise = ConfigItem("wpa_pairwise", "TKIP")
        self.rsn_pairwise = ConfigItem("rsn_pairwise", "CCMP")
        self.hostapd_config_path = "hostapd.conf"
        # interface ip
        self.ip = ip
        # dnsmasq
        self.dhcp_ip_from = dhcp_ip_from
        self.dhcp_ip_to = dhcp_ip_to
        self.netmask = netmask
        self.lease_time = "24h"

    def _check_dependencies(self):
        check = True

        if shutil.which('ifconfig') is None:
            logging.error('hostapd executable not found. Make sure you have installed ifconfig.')
            check = False

        if shutil.which('hostapd') is None:
            logging.error('hostapd executable not found. Make sure you have installed hostapd.')
            check = False

        if shutil.which('dnsmasq') is None:
            logging.error('dnsmasq executable not found. Make sure you have installed dnsmasq.')
            check = False

        return check

    def is_running(self):
        proceses = [proc.name() for proc in psutil.process_iter()]
        return 'hostapd' in proceses or 'dnsmasq' in proceses

    def _write_hostapd_config(self):
        config = self.interface.toString() + self.ssid.toString() + self.wpa_passphrase.toString() + self.driver.toString()\
            + self.hw_mode.toString() + self.channel.toString() + self.macaddr_acl.toString() + self.auth_algs.toString()\
            + self.ignore_broadcast_ssid.toString() + self.wpa.toString() + self.wpa_key_mgmt.toString() + self.wpa_pairwise.toString()\
            + self.rsn_pairwise.toString()
        with open(self.hostapd_config_path, 'w') as hostapd_config_file: hostapd_config_file.write(config)

        logging.debug("hostapd config created to '%s'.", self.hostapd_config_path)
    
    def start(self):
        if not self._check_dependencies():
            return False

        if self.is_running():
            logging.debug("already started.")
            return True

        self._write_hostapd_config()

        try:
            logging.debug('stoping wpa_supplicant.')
            c1 = Execte('killall wpa_supplicant')
            c1.do()
            c1.print()

            logging.debug('turning off radio wifi.')
            c2 = Execte('nmcli radio wifi off')
            c2.do()
            c2.print()

            logging.debug('unblocking wlan.')
            c3 = Execte('rfkill unblock wlan')
            c3.do()
            c3.print()

            logging.debug('waiting 1 sec.')
            time.sleep(1)

        except:
            pass

        logging.debug('interface: {} on IP: {} is up.'.format(self.interface.value, self.ip))
        c4 = Execte('ifconfig {} up {} netmask {}'.format(self.interface.value, self.ip, self.netmask))
        c4.do()
        c4.print()

        logging.debug('waiting 2 sec.')
        time.sleep(2)

        logging.debug('running dnsmasq.')
        c5 = Execte('dnsmasq --dhcp-authoritative --interface={} --dhcp-range={},{},{},{}'\
            .format(self.interface.value, self.dhcp_ip_from, self.dhcp_ip_to, self.netmask, self.lease_time))
        c5.do()
        c5.print()

        logging.debug('waiting 2 sec.')
        time.sleep(2)

        logging.debug('running hostapd.')
        c6 = Execte('hostapd -B {}'.format(self.hostapd_config_path))
        c6.do()
        c6.print()

        logging.debug('hotspot is running.')

        return True

    def stop(self):

        if not self.is_running():
            logging.debug("not running.")
            return True

        # bring down the interface
        logging.debug('interface {} is down.'.format(self.interface.value))
        c1 = Execte('ifconfig {} down'.format(self.interface.value))
        c1.do()
        c1.print()

        # stop hostapd
        logging.debug('stopping hostapd.')
        c2 = Execte('pkill hostapd')
        c2.do()
        c2.print()

        # stop dnsmasq
        logging.debug('stopping dnsmasq.')
        c3 = Execte('killall dnsmasq')
        c3.do()
        c3.print()

        logging.debug('hotspot has stopped.')
        return True

    def restart(self):
        self.stop()
        time.sleep(2)
        self.start()
