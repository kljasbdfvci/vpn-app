from pathlib import Path
import os
import json
import logging

# local
from .Execte import *
from ...setting.models import *

class Network:
    def __init__(self):
        self.list = {
            "lanconfig": {
                "up_file" : Path(__file__).resolve().parent / "template/lanconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template/lanconfig_down.sh",
                "log_file" : "/tmp/lanconfig.log",
            },
            "wlanconfig": {
                "up_file" : Path(__file__).resolve().parent / "template/wlanconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template/wlanconfig_down.sh",
                "log_file" : "/tmp/wlanconfig.log",
            },
            "hotspotconfig": {
                "up_file" : Path(__file__).resolve().parent / "template/hotspotconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template/hotspotconfig_down.sh",
                "log_file" : "/tmp/hotspotconfig.log",
            },
            "dhcpserverconfig": {
                "up_file" : Path(__file__).resolve().parent / "template/dhcpserverconfig_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template/dhcpserverconfig_down.sh",
                "log_file" : "/tmp/dhcpserverconfig.log",
            },
        }
        
        self.lanConfig = LanConfig.objects.all()
        self.wlanConfig = WlanConfig.objects.all()
        self.hotspotConfig = HotspotConfig.objects.first()
        self.dhcpServerConfig = DhcpServerConfig.objects.all()
        self.setting = Setting.objects.first()

    def Apply(self):

        # lanConfig
        for lan in self.lanConfig:
            up_file = self.list["lanconfig"]["up_file"]
            interface = ""
            if lan.interface != "":
                interface = "--interface {}".format(lan.interface)
            dhcp = ""
            if lan.dhcp == True:
                dhcp = "--dhcp"
            ip_address_1 = ""
            if lan.ip_address_1 != "":
                ip_address_1 = "--ip_address_1 {}".format(lan.ip_address_1)
            subnet_mask_1 = ""
            if lan.subnet_mask_1 != "":
                subnet_mask_1 = "--subnet_mask_1 {}".format(lan.subnet_mask_1)
            ip_address_2 = ""
            if lan.ip_address_2 != "":
                ip_address_2 = "--ip_address_2 {}".format(lan.ip_address_2)
            subnet_mask_2 = ""
            if lan.subnet_mask_2 != "":
                subnet_mask_2 = "--subnet_mask_2 {}".format(lan.subnet_mask_2)
            ip_address_3 = ""
            if lan.ip_address_3 != "":
                ip_address_3 = "--ip_address_3 {}".format(lan.ip_address_3)
            subnet_mask_3 = ""
            if lan.subnet_mask_3 != "":
                subnet_mask_3 = "--subnet_mask_3 {}".format(lan.subnet_mask_3)
            ip_address_4 = ""
            if lan.ip_address_4 != "":
                ip_address_4 = "--ip_address_4 {}".format(lan.ip_address_4)
            subnet_mask_4 = ""
            if lan.subnet_mask_4 != "":
                subnet_mask_4 = "--subnet_mask_4 {}".format(lan.subnet_mask_4)
            log_file = self.list["lanconfig"]["log_file"]
            c = Execte("{} {} {} {} {} {} {} {} {} {} {} &> {}".format(\
                up_file, interface, dhcp,\
                ip_address_1, subnet_mask_1,\
                ip_address_2, subnet_mask_2,\
                ip_address_3, subnet_mask_3,\
                ip_address_4, subnet_mask_4,\
                log_file)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()
