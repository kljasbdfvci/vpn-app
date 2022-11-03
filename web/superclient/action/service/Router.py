from pathlib import Path
import os

# local
from .Execte import *
from ...vpn.models import *
from ...hotspot.models import *

class Router:
    def __init__(self,vpn : Configuration, hotspot : Profile):
        self.VpnList = {
            "anyconnect": {
                "up_file" : Path(__file__).resolve().parent / "template/up_aynconnect.sh",
                "pid_file" : Path(__file__).resolve().parent / "anyconnect.pid",
                "interface" : "tun0"
            },
        }
        self.vpn = vpn
        self.hotspot = hotspot

    def ConnectVPN(self, timeout, try_count):
        res = -1
        output = ""
        if isinstance(self.vpn, CiscoConfig):
            up_file = self.VpnList["anyconnect"]["up_file"]
            gateway = self.vpn.host + ":" + str(self.vpn.port)
            username = self.vpn.username
            password = self.vpn.password
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            interface = self.VpnList["anyconnect"]["interface"]
            no_dtls = self.vpn.no_dtls
            passtos = self.vpn.passtos
            no_deflate = self.vpn.no_deflate
            deflate = self.vpn.deflate
            no_http_keepalive = self.vpn.no_http_keepalive
            c1 = Execte("{} {} {} {} {} {} {} {} {} {} {} {} {}".format(\
                up_file, gateway, username, password, timeout, pid_file, interface, try_count, no_dtls, passtos, no_deflate, deflate, no_http_keepalive)
            )
            c1.do()
            res = c1.returncode
            output = c1.stdout + c1.stderr
        else:
            res = -1
            output = "Not Implimnet Yet"

        if res == 0:
            self.reset_ip_table()
            self.set_ip_table()

        return res, output

    def DisconnectVPN(self):
        res = -1
        output = ""
        if isinstance(self.vpn, CiscoConfig):
            pid = self.read_pid_file()
            if pid != 0:
                if self.is_running():
                    c2 = Execte("kill -SIGINT {} || kill -SIGKILL {})".format(pid, pid))
                    c2.do()
                    res = c2.returncode
                    output = c2.stdout + c2.stderr
                else:
                    res = 0
                    output = "vpn is already disable."
                self.delete_pid_file()
            else:
                res = 0
                output = "vpn is already disable."
        else:
            res = -1
            output = "Not Implimnet Yet"

        self.reset_ip_table()

        return res, output

    def is_running(self):
        res = False
        if isinstance(self.vpn, CiscoConfig):
            pid = self.read_pid_file()
            if pid != 0:
                c1 = Execte("kill -0 {})".format(pid))
                c1.do()
                if c1.isSuccess:
                    res = True
        else:
            pass

        return res

    def read_pid_file(self):
        pid = 0
        if isinstance(self.vpn, CiscoConfig):
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            if os.path.isfile(pid_file):
                file = open(pid_file, "r")
                pid = file.read().strip()
        else:
            pass

        return pid

    def delete_pid_file(self):
        if isinstance(self.vpn, CiscoConfig):
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            if os.path.isfile(pid_file):
                os.remove(pid_file)
        else:
            pass

    def set_ip_table(self):

        if isinstance(self.vpn, CiscoConfig):
            hotspot_interface = self.hotspot.interface
            vpn_interface = self.VpnList["anyconnect"]["interface"]
            # sysctl -w net.ipv4.ip_forward=1
            c = Execte("sysctl -w net.ipv4.ip_forward=1")
            c.do()
            # iptables -t nat -A POSTROUTING -o tun0 -j MASQUERADE
            c = Execte("iptables -t nat -A POSTROUTING -o {} -j MASQUERADE".format(vpn_interface))
            c.do()
            # iptables -A FORWARD -i tun0 -o wlan0 -j ACCEPT -m state --state RELATED,ESTABLISHED
            c = Execte("iptables -A FORWARD -i {} -o {} -j ACCEPT -m state --state RELATED,ESTABLISHED".format(vpn_interface, hotspot_interface))
            c.do()
            # iptables -A FORWARD -i wlan0 -o tun0 -j ACCEPT
            c = Execte("iptables -A FORWARD -i {} -o {} -j ACCEPT".format(hotspot_interface, vpn_interface))
            c.do()
            # iptables -A OUTPUT --out-interface wlan0 -j ACCEPT
            c = Execte("iptables -A OUTPUT --out-interface {} -j ACCEPT".format(hotspot_interface))
            c.do()
            # iptables -A INPUT --in-interface wlan0 -j ACCEPT
            c = Execte("iptables -A INPUT --in-interface {} -j ACCEPT".format(hotspot_interface))
            c.do()
            res = 0
        else:
            res = -1

        return res

    def reset_ip_table(self):

        # sysctl -w net.ipv4.ip_forward=0
        c = Execte("sysctl -w net.ipv4.ip_forward=0")
        c.do()
        # iptables -P INPUT ACCEPT
        c = Execte("iptables -P INPUT ACCEPT")
        c.do()
        # iptables -P FORWARD ACCEPT
        c = Execte("iptables -P FORWARD ACCEPT")
        c.do()
        # iptables -P OUTPUT ACCEPT
        c = Execte("iptables -P OUTPUT ACCEPT")
        c.do()
        # iptables -F
        c = Execte("iptables -F")
        c.do()
        # iptables -X
        c = Execte("iptables -X")
        c.do()
        # iptables -t nat -F
        c = Execte("iptables -t nat -F")
        c.do()
        # iptables -t nat -X
        c = Execte("iptables -t nat -X")
        c.do()
        # iptables -t mangle -F
        c = Execte("iptables -t mangle -F")
        c.do()
        # iptables -t mangle -X
        c = Execte("iptables -t mangle -X")
        c.do()
        
        return 0
