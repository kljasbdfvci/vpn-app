from pathlib import Path
import os
import json
import logging

# local
from .Execte import *
from ...vpn.models import *
from ...hotspot.models import *

class Router:
    def __init__(self, vpn : Configuration, hotspot : Profile):
        self.VpnList = {
            "reset_iptables_file" : Path(__file__).resolve().parent / "reset_iptables.sh",
            "anyconnect": {
                "up_file" : Path(__file__).resolve().parent / "template/aynconnect_up.sh",
                "pid_file" : Path(__file__).resolve().parent / "anyconnect.pid",
                "set_iptables_file" : Path(__file__).resolve().parent / "template/aynconnect_set_iptables.sh",
                "reset_iptables_file" : Path(__file__).resolve().parent / "template/aynconnect_reset_iptables.sh",
                "interface" : "tun0"
            },
            "v2ray": {
                "up_file" : Path(__file__).resolve().parent / "template/v2ray_up.sh",
                "config_file" : Path(__file__).resolve().parent / "v2ray.config",
                "pid_file" : Path(__file__).resolve().parent / "v2ray.pid",
                "set_iptables_file" : Path(__file__).resolve().parent / "template/v2ray_set_iptables.sh",
                "reset_iptables_file" : Path(__file__).resolve().parent / "template/v2ray_reset_iptables.sh",
            },
        }
        self.vpn = vpn
        self.hotspot = hotspot

    def ConnectVPN(self, timeout, try_count):
        res = -1
        output = ""
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            up_file = self.VpnList["anyconnect"]["up_file"]
            protocol = openconnect.protocol
            gateway = openconnect.host + ":" + str(openconnect.port)
            username = openconnect.username
            password = openconnect.password
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            interface = self.VpnList["anyconnect"]["interface"]
            no_dtls = openconnect.no_dtls
            passtos = openconnect.passtos
            no_deflate = openconnect.no_deflate
            deflate = openconnect.deflate
            no_http_keepalive = openconnect.no_http_keepalive
            
            c = Execte("{} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(\
                up_file, protocol, gateway, username, password, timeout, pid_file, interface, try_count, no_dtls, passtos, no_deflate, deflate, no_http_keepalive)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            config_json = v2ray.config_json
            up_file = self.VpnList["v2ray"]["up_file"]
            config_file = self.VpnList["v2ray"]["config_file"]
            pid_file = self.VpnList["v2ray"]["pid_file"]
            
            f = open(config_file, "w")
            f.write(config_json)
            f.close()

            c = Execte("{} {} {}".format(\
                up_file, config_file, pid_file)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

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
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            pid = self.read_pid_file()
            if pid != 0:
                if self.is_running():
                    c = Execte("kill -SIGINT {} || kill -SIGKILL {})".format(pid, pid))
                    c.do()
                    c.print()
                    res = c.returncode
                    output = c.getSTD()
                else:
                    res = 0
                    output = "vpn is already disable."
                self.delete_pid_file()
            else:
                res = 0
                output = "vpn is already disable."
            
        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            pid = self.read_pid_file()
            if pid != 0:
                if self.is_running():
                    c = Execte("kill -SIGINT {} || kill -SIGKILL {})".format(pid, pid))
                    c.do()
                    c.print()
                    res = c.returncode
                    output = c.getSTD()
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
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            pid = self.read_pid_file()
            if pid != 0:
                c = Execte("kill -0 {})".format(pid))
                c.do()
                c.print()
                if c.isSuccess:
                    res = True

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            pid = self.read_pid_file()
            if pid != 0:
                c = Execte("kill -0 {})".format(pid))
                c.do()
                c.print()
                if c.isSuccess:
                    res = True        
        else:
            pass

        return res

    def read_pid_file(self):
        pid = 0
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            if os.path.isfile(pid_file):
                file = open(pid_file, "r")
                pid = file.read().strip()
        
        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            pid_file = self.VpnList["v2ray"]["pid_file"]
            if os.path.isfile(pid_file):
                file = open(pid_file, "r")
                pid = file.read().strip()

        else:
            pass

        return pid

    def delete_pid_file(self):
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            if os.path.isfile(pid_file):
                os.remove(pid_file)

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            pid_file = self.VpnList["v2ray"]["pid_file"]
            if os.path.isfile(pid_file):
                os.remove(pid_file)

        else:
            pass

    def set_ip_table(self):

        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            hotspot_interface = self.hotspot.interface
            vpn_interface = self.VpnList["anyconnect"]["interface"]
            set_iptables_file = self.VpnList["anyconnect"]["set_iptables_file"]
            c = Execte("{} {} {}".format(set_iptables_file, hotspot_interface, vpn_interface))
            c.do()
            c.print()
            res = c.returncode

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            set_iptables_file = self.VpnList["v2ray"]["set_iptables_file"]
            config_json = v2ray.config_json
            js = json.loads(config_json)
            v2ray_port = js["inbounds"][0]["port"]
            hotspot_interface = self.hotspot.interface
            hotspot_ip = self.hotspot.ip
            hotspot_netmask = self.hotspot.netmask

            c = Execte("{} {} {} {} {} {}".format(set_iptables_file, v2ray_port, hotspot_interface, hotspot_ip, hotspot_netmask, "eth0"))
            c.do()
            c.print()
            res = c.returncode

        else:
            res = -1

        return res

    def reset_ip_table(self):

        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            reset_iptables_file = self.VpnList["anyconnect"]["reset_iptables_file"]
            c = Execte("{}".format(reset_iptables_file))
            c.do()
            c.print()
            res = c.returncode
        else:
            reset_iptables_file = self.VpnList["reset_iptables_file"]
            c = Execte("{}".format(reset_iptables_file))
            c.do()
            c.print()
            res = c.returncode
        
        return res
