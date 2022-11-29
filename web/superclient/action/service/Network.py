from pathlib import Path
import os

# local
from .Execte import *
from ...setting.models import *

class Network:
    def __init__(self):
        self.list = {
            "all" : {
                "down_file" : Path(__file__).resolve().parent / "template_network/all_down.sh",
            },
            "lanconfig": {
                "up_file" : Path(__file__).resolve().parent / "template_network/lanconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_network/lanconfig_down.sh",
            },
            "wlanconfig": {
                "up_file" : Path(__file__).resolve().parent / "template_network/wlanconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_network/wlanconfig_down.sh",
                "wpa_supplicant_config_file" : "/tmp/wpa_supplicant.conf",
                "wpa_supplicant_pid_file" : "/tmp/wpa_supplicant.pid",
                "wpa_supplicant_log_file" : "/tmp/wpa_supplicant.log",
            },
            "hotspotconfig": {
                "up_file" : Path(__file__).resolve().parent / "template_network/hotspotconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_network/hotspotconfig_down.sh",
                "hostapd_config_file" : "/tmp/hostapd.conf",
                "hostapd_pid_file" : "/tmp/hostapd.pid",
                "hostapd_log_file" : "/tmp/hostapd.log",
            },
            "dhcpserverconfig": {
                "up_file" : Path(__file__).resolve().parent / "template_network/dhcpserverconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_network/dhcpserverconfig_down.sh",
                "dnsmasq_pid_file" : "/tmp/dnsmasq_{}.pid",
                "dnsmasq_log_file" : "/tmp/dnsmasq_{}.log",
                "dnsmasq_lease_file" : "/tmp/dnsmasq_{}.leases",
            },
            "dns": {
                "up_file" : Path(__file__).resolve().parent / "template_network/dns_up.sh",
            },
        }
        
        self.lanConfig = LanConfig.objects.all()
        self.wlanConfig = WlanConfig.objects.all()
        self.hotspotConfig = HotspotConfig.objects.first()
        self.dhcpServerConfig = DhcpServerConfig.objects.all()
        self.setting = Setting.objects.first()

    def Apply(self):

        self._reset()

        # lanConfig
        for lan in self.lanConfig:
            if self.is_lan_interface(lan.interface):
                up_file = self.list["lanconfig"]["up_file"]
                interface = "--interface '{}'".format(lan.interface) if lan.interface != "" else ""
                dhcp = "--dhcp" if lan.dhcp else ""
                ip_address_1 = "--ip_address_1 '{}'".format(lan.ip_address_1) if lan.ip_address_1 != "" else ""
                subnet_mask_1 = "--subnet_mask_1 '{}'".format(lan.subnet_mask_1) if lan.subnet_mask_1 != "" else ""
                ip_address_2 = "--ip_address_2 '{}'".format(lan.ip_address_2) if lan.ip_address_2 != "" else ""
                subnet_mask_2 = "--subnet_mask_2 '{}'".format(lan.subnet_mask_2) if lan.subnet_mask_2 != "" else ""
                ip_address_3 = "--ip_address_3 '{}'".format(lan.ip_address_3) if lan.ip_address_3 != "" else ""
                subnet_mask_3 = "--subnet_mask_3 '{}'".format(lan.subnet_mask_3) if lan.subnet_mask_3 != "" else ""
                ip_address_4 = "--ip_address_4 '{}'".format(lan.ip_address_4) if lan.ip_address_4 != "" else ""
                subnet_mask_4 = "--subnet_mask_4 '{}'".format(lan.subnet_mask_4) if lan.subnet_mask_4 != "" else ""

                c = Execte("{} {} {} {} {} {} {} {} {} {} {}".format(\
                    up_file, interface, dhcp,\
                    ip_address_1, subnet_mask_1,\
                    ip_address_2, subnet_mask_2,\
                    ip_address_3, subnet_mask_3,\
                    ip_address_4, subnet_mask_4), True
                )
                c.do()
                c.print()
                res = c.returncode
                output = c.getSTD()

        # wlanConfig
        for wlan in self.wlanConfig:
            if self.is_wlan_interface(wlan.interface):
                up_file = self.list["wlanconfig"]["up_file"]
                interface = "--interface '{}'".format(wlan.interface) if wlan.interface != "" else ""
                ssid = "--ssid '{}'".format(wlan.ssid)
                wpa_passphrase = "--wpa_passphrase '{}'".format(wlan.wpa_passphrase)
                driver = "--driver '{}'".format(wlan.driver)
                wpa_supplicant_config_file = "--wpa_supplicant_config_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_config_file"])
                wpa_supplicant_pid_file = "--wpa_supplicant_pid_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_pid_file"])
                wpa_supplicant_log_file = "--wpa_supplicant_log_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_log_file"])
                dhcp = "--dhcp" if wlan.dhcp else ""
                ip_address_1 = "--ip_address_1 '{}'".format(wlan.ip_address_1) if wlan.ip_address_1 != "" else ""
                subnet_mask_1 = "--subnet_mask_1 '{}'".format(wlan.subnet_mask_1) if wlan.subnet_mask_1 != "" else ""
                ip_address_2 = "--ip_address_2 '{}'".format(wlan.ip_address_2) if wlan.ip_address_2 != "" else ""
                subnet_mask_2 = "--subnet_mask_2 '{}'".format(wlan.subnet_mask_2) if wlan.subnet_mask_2 != "" else ""
                ip_address_3 = "--ip_address_3 '{}'".format(wlan.ip_address_3) if wlan.ip_address_3 != "" else ""
                subnet_mask_3 = "--subnet_mask_3 '{}'".format(wlan.subnet_mask_3) if wlan.subnet_mask_3 != "" else ""
                ip_address_4 = "--ip_address_4 '{}'".format(wlan.ip_address_4) if wlan.ip_address_4 != "" else ""
                subnet_mask_4 = "--subnet_mask_4 '{}'".format(wlan.subnet_mask_4) if wlan.subnet_mask_4 != "" else ""
                c = Execte("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(\
                    up_file, interface, ssid, wpa_passphrase, driver,\
                    wpa_supplicant_config_file, wpa_supplicant_pid_file, wpa_supplicant_log_file,\
                    dhcp,\
                    ip_address_1, subnet_mask_1,\
                    ip_address_2, subnet_mask_2,\
                    ip_address_3, subnet_mask_3,\
                    ip_address_4, subnet_mask_4), True
                )
                c.do()
                c.print()
                res = c.returncode
                output = c.getSTD()

        # hotspotConfig
        hotspot = self.hotspotConfig
        if hotspot != None and self.is_wlan_interface(hotspot.interface):
            up_file = self.list["hotspotconfig"]["up_file"]
            interface = "--interface '{}'".format(hotspot.interface)
            channel = "--channel '{}'".format(hotspot.channel)
            ssid = "--ssid '{}'".format(hotspot.ssid)
            wpa_passphrase = "--wpa_passphrase '{}'".format(hotspot.wpa_passphrase)
            hostapd_config_file = "--hostapd_config_file '{}'".format(self.list["hotspotconfig"]["hostapd_config_file"])
            hostapd_pid_file = "--hostapd_pid_file '{}'".format(self.list["hotspotconfig"]["hostapd_pid_file"])
            hostapd_log_file = "--hostapd_log_file '{}'".format(self.list["hotspotconfig"]["hostapd_log_file"])
            c = Execte("{} {} {} {} {} {} {} {}".format(\
                up_file, interface, channel, ssid, wpa_passphrase,\
                hostapd_config_file, hostapd_pid_file, hostapd_log_file)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

        # dhcpServerConfig
        for dhcpServer in self.dhcpServerConfig:
            if self.is_interface(dhcpServer.interface):
                up_file = self.list["dhcpserverconfig"]["up_file"]
                interface = "--interface '{}'".format(dhcpServer.interface)
                ip_address = "--ip_address '{}'".format(dhcpServer.ip_address)
                subnet_mask = "--subnet_mask '{}'".format(dhcpServer.subnet_mask)
                dhcp_ip_address_from = "--dhcp_ip_address_from '{}'".format(dhcpServer.dhcp_ip_address_from)
                dhcp_ip_address_to = "--dhcp_ip_address_to '{}'".format(dhcpServer.dhcp_ip_address_to)
                dns_server = ""
                if self.setting.dns_Mode == self.setting.DnsMode._3 and self.setting.dns != "":
                    dns_list = self.setting.dns.split(",")
                    for i in range(len(dns_list)):
                        dns_list[i] = "/#/" + dns_list[i]
                    dns_server = "--dns_server '{}'".format(",".join(dns_list))
                dnsmasq_pid_file = "--dnsmasq_pid_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_pid_file"].format(dhcpServer.interface))
                dnsmasq_log_file = "--dnsmasq_log_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_log_file"].format(dhcpServer.interface))
                dnsmasq_lease_file = "--dnsmasq_lease_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_lease_file"].format(dhcpServer.interface))
                c = Execte("{} {} {} {} {} {} {} {} {} {}".format(\
                    up_file, interface, ip_address, subnet_mask,\
                    dhcp_ip_address_from, dhcp_ip_address_to,\
                    dns_server,\
                    dnsmasq_pid_file, dnsmasq_log_file, dnsmasq_lease_file)
                )
                c.do()
                c.print()
                res = c.returncode
                output = c.getSTD()

        # dns
        if self.setting.dns == self.setting.DnsMode._2 and self.setting.dns != "":
            up_file = self.list["dns"]["up_file"]
            dns_server = "--dns_server '{}'".format(self.setting.dns)
            c = Execte("{} {}".format(\
                up_file, dns_server)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

    def _reset(self):
        # all_down
        down_file = self.list["all"]["down_file"]
        wpa_supplicant_config_file = "--wpa_supplicant_config_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_config_file"])
        wpa_supplicant_pid_file = "--wpa_supplicant_pid_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_pid_file"])
        wpa_supplicant_log_file = "--wpa_supplicant_log_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_log_file"])
        hostapd_config_file = "--hostapd_config_file '{}'".format(self.list["hotspotconfig"]["hostapd_config_file"])
        hostapd_pid_file = "--hostapd_pid_file '{}'".format(self.list["hotspotconfig"]["hostapd_pid_file"])
        hostapd_log_file = "--hostapd_log_file '{}'".format(self.list["hotspotconfig"]["hostapd_log_file"])
        dnsmasq_pid_file = "--dnsmasq_pid_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_pid_file"].format("*"))
        dnsmasq_log_file = "--dnsmasq_log_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_log_file"].format("*"))
        dnsmasq_lease_file = "--dnsmasq_lease_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_lease_file"].format("*"))
        c = Execte("{} {} {} {} {} {} {} {} {} {}".format(\
            down_file,
            wpa_supplicant_config_file, wpa_supplicant_pid_file, wpa_supplicant_log_file,\
            hostapd_config_file, hostapd_pid_file, hostapd_log_file,\
            dnsmasq_pid_file, dnsmasq_log_file, dnsmasq_lease_file)
        )
        c.do()
        c.print()
        res = c.returncode
        output = c.getSTD()

    def get_interfaces(self):
        return self.get_lan_interfaces() + self.get_wlan_interfaces()

    def is_interface(self, interface):
        res = True if interface in self.get_interfaces() else False
        return res

    def get_lan_interfaces(self):
        c = Execte("nmcli device status | grep ethernet | cut -d " " -f1")
        c.do()
        addrs = c.stdout.split("\n")
        addrs.sort()
        return addrs
    
    def is_lan_interface(self, interface):
        res = True if interface in self.get_lan_interfaces() else False
        return res

    def get_first_lan_interface(self):
        return self.get_lan_interfaces()[0]

    def get_wlan_interfaces(self):
        #addrs = []
        #for path in os.listdir("/sys/class/net"):
        #    if os.path.isdir("/sys/class/net/" + path + "/wireless"):
        #        addrs.append(path)
        #addrs.sort()
        c = Execte("nmcli device status | grep wifi | cut -d " " -f1")
        c.do()
        addrs = c.stdout.split("\n")
        addrs.sort()
        return addrs

    def is_wlan_interface(self, interface):
        res = True if interface in self.get_wlan_interfaces() else False
        return res

    def get_first_wlan_interface(self):
        return self.get_wlan_interfaces()[0]
