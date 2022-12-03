from pathlib import Path
import os

# local
from .Execte import *
from .Network_Util import *
from ...setting.models import *

class Network:
    def __init__(self):
        self.list = {
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
                "dhcpd_write_file" : Path(__file__).resolve().parent / "template_network/dhcpserverconfig_dhcpd_write.sh",
                "dhcpd_config_file" : "/tmp/dhcpd.config",
                "dhcpd_pid_file" : "/tmp/dhcpd.pid",
                "dhcpd_log_file" : "/tmp/dhcpd.log",
                "dhcpd_lease_file" : "/tmp/dhcpd.lease",
                "named_config_file" : "/tmp/named.conf"
            },
            "dns": {
                "up_file" : Path(__file__).resolve().parent / "template_network/dns_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_network/dns_down.sh",
                "manage_up" : "python3 {} network_apply_dns".format(Path(__file__).resolve().parent.parent.parent.parent / "manage.py")
            },
            "iptables": {
                "up_file" : Path(__file__).resolve().parent / "template_network/iptables_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_network/iptables_down.sh",
            },
        }
        
        self.lanConfig = LanConfig.objects.all()
        self.wlanConfig = WlanConfig.objects.all()
        self.hotspotConfig = HotspotConfig.objects.first()
        self.dhcpServerConfig = DhcpServerConfig.objects.all()
        self.general = General.objects.first()

    def Apply(self):
        self.ApplyLanConfig()
        self.ApplyWlanConfig()
        self.ApplyHotspotConfig()
        self.ApplyDhcpServerConfig()
        self.ApplyDns()
        self.ApplyIptables()

    def Down(self):
        self.DownLanConfig()
        self.DownWlanConfig()
        self.DownHotspotConfig()
        self.DownDhcpServerConfig()
        self.DownDns()
        self.DownIptables()

    def Up(self):
        self.UpLanConfig()
        self.UpWlanConfig()
        self.UpHotspotConfig()
        self.UpDhcpServerConfig()
        self.UpDns()
        self.UpIptables()

    def ApplyLanConfig(self):
        self.DownLanConfig()
        self.UpLanConfig()

    def DownLanConfig(self):
        # lanConfig down
        down_file = self.list["lanconfig"]["down_file"]
        c = Execte("{}".format(\
            down_file)
        )
        c.do()
        c.print()

    def UpLanConfig(self):
        # lanConfig up
        for lan in self.lanConfig:
            if Network_Util().is_lan_interface(lan.interface):
                up_file = self.list["lanconfig"]["up_file"]
                interface = "--interface '{}'".format(lan.interface) if lan.interface != "" else ""
                dhcp = "--dhcp" if lan.dhcp else ""
                dns_manage_up = "--dns_manage_up '{}'".format(self.list["dns"]["manage_up"])
                ip_address_1 = "--ip_address_1 '{}'".format(lan.ip_address_1) if lan.ip_address_1 != "" else ""
                subnet_mask_1 = "--subnet_mask_1 '{}'".format(lan.subnet_mask_1) if lan.subnet_mask_1 != "" else ""
                ip_address_2 = "--ip_address_2 '{}'".format(lan.ip_address_2) if lan.ip_address_2 != "" else ""
                subnet_mask_2 = "--subnet_mask_2 '{}'".format(lan.subnet_mask_2) if lan.subnet_mask_2 != "" else ""
                ip_address_3 = "--ip_address_3 '{}'".format(lan.ip_address_3) if lan.ip_address_3 != "" else ""
                subnet_mask_3 = "--subnet_mask_3 '{}'".format(lan.subnet_mask_3) if lan.subnet_mask_3 != "" else ""
                ip_address_4 = "--ip_address_4 '{}'".format(lan.ip_address_4) if lan.ip_address_4 != "" else ""
                subnet_mask_4 = "--subnet_mask_4 '{}'".format(lan.subnet_mask_4) if lan.subnet_mask_4 != "" else ""

                c = Execte("{} {} {} {} {} {} {} {} {} {} {} {}".format(\
                    up_file, interface, dhcp, dns_manage_up,
                    ip_address_1, subnet_mask_1,\
                    ip_address_2, subnet_mask_2,\
                    ip_address_3, subnet_mask_3,\
                    ip_address_4, subnet_mask_4), True
                )
                c.do()
                c.print()

    def ApplyWlanConfig(self):
        self.DownWlanConfig()
        self.UpWlanConfig()

    def DownWlanConfig(self):
        # wlanConfig down
        down_file = self.list["wlanconfig"]["down_file"]
        wpa_supplicant_config_file = "--wpa_supplicant_config_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_config_file"])
        wpa_supplicant_pid_file = "--wpa_supplicant_pid_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_pid_file"])
        wpa_supplicant_log_file = "--wpa_supplicant_log_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_log_file"])
        c = Execte("{} {} {} {}".format(\
            down_file,
            wpa_supplicant_config_file, wpa_supplicant_pid_file, wpa_supplicant_log_file)
        )
        c.do()
        c.print()

    def UpWlanConfig(self):
        # wlanConfig up
        for wlan in self.wlanConfig:
            if Network_Util().is_wlan_interface(wlan.interface):
                up_file = self.list["wlanconfig"]["up_file"]
                interface = "--interface '{}'".format(wlan.interface) if wlan.interface != "" else ""
                ssid = "--ssid '{}'".format(wlan.ssid)
                wpa_passphrase = "--wpa_passphrase '{}'".format(wlan.wpa_passphrase)
                driver = "--driver '{}'".format(wlan.driver)
                wpa_supplicant_config_file = "--wpa_supplicant_config_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_config_file"])
                wpa_supplicant_pid_file = "--wpa_supplicant_pid_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_pid_file"])
                wpa_supplicant_log_file = "--wpa_supplicant_log_file '{}'".format(self.list["wlanconfig"]["wpa_supplicant_log_file"])
                dhcp = "--dhcp" if wlan.dhcp else ""
                dns_manage_up = "--dns_manage_up '{}'".format(self.list["dns"]["manage_up"])
                ip_address_1 = "--ip_address_1 '{}'".format(wlan.ip_address_1) if wlan.ip_address_1 != "" else ""
                subnet_mask_1 = "--subnet_mask_1 '{}'".format(wlan.subnet_mask_1) if wlan.subnet_mask_1 != "" else ""
                ip_address_2 = "--ip_address_2 '{}'".format(wlan.ip_address_2) if wlan.ip_address_2 != "" else ""
                subnet_mask_2 = "--subnet_mask_2 '{}'".format(wlan.subnet_mask_2) if wlan.subnet_mask_2 != "" else ""
                ip_address_3 = "--ip_address_3 '{}'".format(wlan.ip_address_3) if wlan.ip_address_3 != "" else ""
                subnet_mask_3 = "--subnet_mask_3 '{}'".format(wlan.subnet_mask_3) if wlan.subnet_mask_3 != "" else ""
                ip_address_4 = "--ip_address_4 '{}'".format(wlan.ip_address_4) if wlan.ip_address_4 != "" else ""
                subnet_mask_4 = "--subnet_mask_4 '{}'".format(wlan.subnet_mask_4) if wlan.subnet_mask_4 != "" else ""
                c = Execte("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(\
                    up_file, interface, ssid, wpa_passphrase, driver,\
                    wpa_supplicant_config_file, wpa_supplicant_pid_file, wpa_supplicant_log_file,\
                    dhcp, dns_manage_up,\
                    ip_address_1, subnet_mask_1,\
                    ip_address_2, subnet_mask_2,\
                    ip_address_3, subnet_mask_3,\
                    ip_address_4, subnet_mask_4), True
                )
                c.do()
                c.print()

    def ApplyHotspotConfig(self):
        self.DownHotspotConfig()
        self.UpHotspotConfig()

    def DownHotspotConfig(self):
        # hotspotConfig down
        down_file = self.list["hotspotconfig"]["down_file"]
        hostapd_config_file = "--hostapd_config_file '{}'".format(self.list["hotspotconfig"]["hostapd_config_file"])
        hostapd_pid_file = "--hostapd_pid_file '{}'".format(self.list["hotspotconfig"]["hostapd_pid_file"])
        hostapd_log_file = "--hostapd_log_file '{}'".format(self.list["hotspotconfig"]["hostapd_log_file"])
        c = Execte("{} {} {} {}".format(\
            down_file,\
            hostapd_config_file, hostapd_pid_file, hostapd_log_file)
        )
        c.do()
        c.print()

    def UpHotspotConfig(self):
        # hotspotConfig up
        hotspot = self.hotspotConfig
        if hotspot != None and Network_Util().is_wlan_interface(hotspot.interface):
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

    def ApplyDhcpServerConfig(self):
        self.DownDhcpServerConfig()
        self.UpDhcpServerConfig()

    def DownDhcpServerConfig(self):
        # dhcpServerConfig down
        down_file = self.list["dhcpserverconfig"]["down_file"]
        dnsmasq_pid_file = "--dnsmasq_pid_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_pid_file"].format("*"))
        dnsmasq_log_file = "--dnsmasq_log_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_log_file"].format("*"))
        dnsmasq_lease_file = "--dnsmasq_lease_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_lease_file"].format("*"))
        c = Execte("{} {} {} {}".format(\
            down_file,
            dnsmasq_pid_file, dnsmasq_log_file, dnsmasq_lease_file)
        )
        c.do()
        c.print()

    def UpDhcpServerConfig(self):
        # dhcpServerConfig up
        flag_dhcpd = 0
        interface_dhcpd = ""
        for dhcpServer in self.dhcpServerConfig:
            if Network_Util().is_interface(dhcpServer.interface) and dhcpServer.dhcp_module == DhcpServerConfig.DhcpModule.dnsmasq:
                up_file = self.list["dhcpserverconfig"]["up_file"]
                dhcp_module = "--dhcp_module '{}'".format(dhcpServer.dhcp_module)
                interface = "--interface '{}'".format(dhcpServer.interface)
                ip_address = "--ip_address '{}'".format(dhcpServer.ip_address)
                subnet_mask = "--subnet_mask '{}'".format(dhcpServer.subnet_mask)
                dhcp_ip_address_from = "--dhcp_ip_address_from '{}'".format(dhcpServer.dhcp_ip_address_from)
                dhcp_ip_address_to = "--dhcp_ip_address_to '{}'".format(dhcpServer.dhcp_ip_address_to)
                dns_server = ""
                #if self.general.dns_Mode == self.general.DnsMode._3 and self.general.dns != "":
                #    dns_list = self.general.dns.split(",")
                #    for i in range(len(dns_list)):
                #        dns_list[i] = "/#/" + dns_list[i]
                #    dns_server = "--dns_server '{}'".format(",".join(dns_list))
                dnsmasq_pid_file = "--dnsmasq_pid_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_pid_file"].format(dhcpServer.interface))
                dnsmasq_log_file = "--dnsmasq_log_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_log_file"].format(dhcpServer.interface))
                dnsmasq_lease_file = "--dnsmasq_lease_file '{}'".format(self.list["dhcpserverconfig"]["dnsmasq_lease_file"].format(dhcpServer.interface))
                c = Execte("{} {} {} {} {} {} {} {} {} {} {}".format(\
                    up_file, dhcp_module, interface, ip_address, subnet_mask,\
                    dhcp_ip_address_from, dhcp_ip_address_to,\
                    dns_server,\
                    dnsmasq_pid_file, dnsmasq_log_file, dnsmasq_lease_file)
                )
                c.do()
                c.print()
            elif Network_Util().is_interface(dhcpServer.interface) and dhcpServer.dhcp_module == DhcpServerConfig.DhcpModule.dhcpd:
                dhcpd_write_file = self.list["dhcpserverconfig"]["dhcpd_write_file"]
                interface = "--interface '{}'".format(dhcpServer.interface)
                ip_address = "--ip_address '{}'".format(dhcpServer.ip_address)
                subnet_mask = "--subnet_mask '{}'".format(dhcpServer.subnet_mask)
                dhcp_ip_address_from = "--dhcp_ip_address_from '{}'".format(dhcpServer.dhcp_ip_address_from)
                dhcp_ip_address_to = "--dhcp_ip_address_to '{}'".format(dhcpServer.dhcp_ip_address_to)
                dhcpd_config_file = "--dhcpd_config_file '{}'".format(self.list["dhcpserverconfig"]["dhcpd_config_file"])
                c = Execte("{} {} {} {} {} {} {}".format(\
                    dhcpd_write_file, interface,\
                    ip_address, subnet_mask,\
                    dhcp_ip_address_from, dhcp_ip_address_to,\
                    dhcpd_config_file)
                )
                c.do()
                c.print()
                flag_dhcpd = 1
                interface_dhcpd = interface_dhcpd + " " + dhcpServer.interface

        if flag_dhcpd == 1:
            up_file = self.list["dhcpserverconfig"]["up_file"]
            dhcp_module = "--dhcp_module '{}'".format("isc-dhcp-server")
            interface_dhcpd = "--interface_dhcpd '{}'".format(interface_dhcpd)
            dhcpd_config_file = "--dhcpd_config_file '{}'".format(self.list["dhcpserverconfig"]["dhcpd_config_file"])
            dhcpd_pid_file = "--dhcpd_pid_file '{}'".format(self.list["dhcpserverconfig"]["dhcpd_pid_file"])
            dhcpd_log_file = "--dhcpd_log_file '{}'".format(self.list["dhcpserverconfig"]["dhcpd_log_file"])
            dhcpd_lease_file = "--dhcpd_lease_file '{}'".format(self.list["dhcpserverconfig"]["dhcpd_lease_file"])
            named_config_file = "--named_config_file '{}'".format(self.list["dhcpserverconfig"]["named_config_file"])
            dns_server = "--dns_server {}".format(self.general.dns) if self.general.dns_Mode == self.general.DnsMode._2 and self.general.dns != "" else ""
            if self.general.dns_Mode == self.general.DnsMode._2 and self.general.dns != "":
                pass
            c = Execte("{} {} {} {} {} {} {} {} {}".format(\
                up_file, dhcp_module,\
                interface_dhcpd,\
                dhcpd_config_file, dhcpd_pid_file, dhcpd_log_file, dhcpd_lease_file,\
                named_config_file, dns_server)
            )
            c.do()
            c.print()
        
    def ApplyDns(self):
        self.DownDns()
        self.UpDns()

    def DownDns(self):
        # dns down
        down_file = self.list["dns"]["down_file"]
        c = Execte("{}".format(\
            down_file)
        )
        c.do()
        c.print()


    def UpDns(self):
        # dns up
        if self.general.dns_Mode == self.general.DnsMode._2 and self.general.dns != "":
            up_file = self.list["dns"]["up_file"]
            dns_server = "--dns_server '{}'".format(self.general.dns)
            c = Execte("{} {}".format(\
                up_file, dns_server)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

    def ApplyIptables(self):
        self.DownIptables()
        self.UpIptables()

    def DownIptables(self):
        # iptables down
        down_file = self.list["iptables"]["down_file"]
        c = Execte("{}".format(\
            down_file)
        )
        c.do()
        c.print()

    def UpIptables(self):
        # iptables up
        up_file = self.list["iptables"]["up_file"]
        c = Execte("{}".format(
            up_file)
        )
        c.do()
        c.print()
