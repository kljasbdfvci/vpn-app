# local
from .Execte import *

class Network_Util:

    def get_interfaces(self):
        return self.get_lan_interfaces() + self.get_wlan_interfaces()

    def is_interface(self, interface):
        res = True if interface in self.get_interfaces() else False
        return res

    def get_lan_interfaces(self):
        c = Execte("nmcli device status | grep ethernet | cut -d ' ' -f1")
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
        c = Execte("nmcli device status | grep wifi | cut -d ' ' -f1")
        c.do()
        addrs = c.stdout.strip().split("\n")
        addrs.sort()
        return addrs

    def is_wlan_interface(self, interface):
        res = True if interface in self.get_wlan_interfaces() else False
        return res

    def get_first_wlan_interface(self):
        return self.get_wlan_interfaces()[0]
