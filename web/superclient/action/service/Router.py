from pathlib import Path
import os
import json
import logging

# local
from .Execte import *
from ...vpn.models import *
from ...setting.models import Setting

class Router:
    def __init__(self, vpn : Configuration):
        self.VpnList = {
            "reset_iptables_file" : Path(__file__).resolve().parent / "template_router/reset_iptables.sh",
            "openconnect": {
                "up_file" : Path(__file__).resolve().parent / "template_router/openconnect_up.sh",
                "set_iptables_file" : Path(__file__).resolve().parent / "template_router/openconnect_set_iptables.sh",
                "reset_iptables_file" : Path(__file__).resolve().parent / "template_router/openconnect_reset_iptables.sh",
                "pid_file" : "/tmp/openconnect.pid",
                "log_file" : "/tmp/openconnect.log",
                "interface" : "tun0"
            },
            "v2ray": {
                "up_file" : Path(__file__).resolve().parent / "template_router/v2ray_up.sh",
                "set_iptables_file" : Path(__file__).resolve().parent / "template_router/v2ray_set_iptables.sh",
                "reset_iptables_file" : Path(__file__).resolve().parent / "template_router/v2ray_reset_iptables.sh",
                "pid_file" : "/tmp/v2ray.pid",
                "log_file" : "/tmp/v2ray.log",
                "config_file" : Path(__file__).resolve().parent / "v2ray.config",
                "badvpn-tun2socks_log_file" : "/tmp/badvpn-tun2socks.log",
                "redsocks_config_file" : Path(__file__).resolve().parent / "redsocks.conf",
                "redsocks_log_file" : "/tmp/redsocks.log",
                "dns2socks_log_file" : "/tmp/dns2socks.log",
                "interface" : "tun0"
            },
        }
        self.vpn = vpn
        self.setting = Setting.objects.first()

    def ConnectVPN(self, timeout, try_count):
        res = -1
        output = ""
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass

            up_file = self.VpnList["openconnect"]["up_file"]
            pid_file = self.VpnList["openconnect"]["pid_file"]
            log_file = self.VpnList["openconnect"]["log_file"]

            protocol = openconnect.protocol
            gateway = openconnect.host + ":" + str(openconnect.port)
            username = openconnect.username
            password = openconnect.password
            interface = self.VpnList["openconnect"]["interface"]
            no_dtls = openconnect.no_dtls
            passtos = openconnect.passtos
            no_deflate = openconnect.no_deflate
            deflate = openconnect.deflate
            no_http_keepalive = openconnect.no_http_keepalive
            
            c = Execte("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(\
                up_file, pid_file, log_file, timeout, try_count, \
                protocol, gateway, username, password, interface, no_dtls, passtos, no_deflate, deflate, no_http_keepalive)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            
            up_file = self.VpnList["v2ray"]["up_file"]
            pid_file = self.VpnList["v2ray"]["pid_file"]
            log_file = self.VpnList["v2ray"]["log_file"]

            config_file = self.VpnList["v2ray"]["config_file"]
            config_json = v2ray.config_json
            
            f = open(config_file, "w")
            f.write(config_json)
            f.close()

            c = Execte("{} {} {} {} {} {}".format(\
                up_file, pid_file, log_file, timeout, try_count, \
                config_file)
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
                    c = Execte("kill -2 {} || kill -9 {}".format(pid, pid))
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
                    c = Execte("kill -2 {} || kill -9 {}".format(pid, pid))
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
                c = Execte("kill -0 {}".format(pid))
                c.do()
                c.print()
                if c.isSuccess:
                    res = True

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            pid = self.read_pid_file()
            if pid != 0:
                c = Execte("kill -0 {}".format(pid))
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
            pid_file = self.VpnList["openconnect"]["pid_file"]
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
            pid_file = self.VpnList["openconnect"]["pid_file"]
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
            set_iptables_file = self.VpnList["openconnect"]["set_iptables_file"]

            c = Execte("{}".format(set_iptables_file))
            c.do()
            c.print()
            res = c.returncode

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            set_iptables_file = self.VpnList["v2ray"]["set_iptables_file"]
            vpn_interface = self.VpnList["v2ray"]["interface"]
            config_json = v2ray.config_json
            js = json.loads(config_json)
            v2ray_inbounds_port = js["inbounds"][0]["port"]
            v2ray_outbounds_ip = js["outbounds"][0]["settings"]["vnext"][0]["address"]
            badvpn_tun2socks_log_file = self.VpnList["v2ray"]["badvpn-tun2socks_log_file"]
            dns_mode = self.setting.DnsMode._1 if self.setting.dns == "" else self.setting.dns_Mode
            dns_server = ""
            dns_log = ""
            if dns_mode == self.setting.DnsMode._4:
                dns_server = self.setting.dns.split(",")[0]
                dns_log = self.VpnList["v2ray"]["dns2socks_log_file"]

            c = Execte("{} {} {} {} {} {} {} {}".format(\
                set_iptables_file,\
                vpn_interface,\
                v2ray_inbounds_port, v2ray_outbounds_ip,\
                badvpn_tun2socks_log_file,\
                dns_mode, dns_server, dns_log)
            )
            c.do()
            c.print()
            res = c.returncode

        else:
            res = -1

        return res

    def reset_ip_table(self):

        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            reset_iptables_file = self.VpnList["openconnect"]["reset_iptables_file"]
            c = Execte("{}".format(reset_iptables_file))
            c.do()
            c.print()
            res = c.returncode

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            reset_iptables_file = self.VpnList["v2ray"]["reset_iptables_file"]
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
