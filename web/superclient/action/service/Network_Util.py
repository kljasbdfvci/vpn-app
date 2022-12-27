from pathlib import Path

# local
from .Execte import *

class Network_Util:

    def __init__(self):
        self.interface_list = Path(__file__).resolve().parent / "template_network/interface_list.sh"

    def get_interfaces(self):
        return self.get_lan_interfaces() + self.get_wlan_interfaces()

    def is_interface(self, interface):
        res = True if interface in self.get_interfaces() else False
        return res

    def get_lan_interfaces(self):
        c = Execte("{} {}".format(self.interface_list, "eth"))
        c.do()
        addrs = c.stdout.strip().split("\n")
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
        c = Execte("{} {}".format(self.interface_list, "wlan"))
        c.do()
        addrs = c.stdout.strip().split("\n")
        addrs.sort()
        return addrs

    def is_wlan_interface(self, interface):
        res = True if interface in self.get_wlan_interfaces() else False
        return res

    def get_first_wlan_interface(self):
        return self.get_wlan_interfaces()[0]

    def get_mac(self, interface):
        if self.is_interface(interface):
            return self._get_mac(interface)
        else:
            return None

    def _get_mac(self, interface):
        f = open("/sys/class/net/" + interface + "/address", "r")
        return f.read().strip()

    def get_interface_by_mac(self, mac):
        addrs = self.get_interfaces()
        for addr in addrs:
            if mac == self._get_mac(addr):
                return addr
        return None
