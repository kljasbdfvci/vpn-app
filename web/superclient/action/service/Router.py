from pathlib import Path
import os
import json
import random

# local
from .Execte import *
from ...vpn.models import *
from ...setting.models import *

class Router:
    def __init__(self, vpn : Configuration):
        self.VpnList = {
            "openconnect": {
                "up_file" : Path(__file__).resolve().parent / "template_router/openconnect_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_router/openconnect_down.sh",
                "pid_file" : "/tmp/openconnect.pid",
                "log_file" : "/tmp/openconnect.log",
                "interface" : "tun0"
            },
            "v2ray": {
                "up_file" : Path(__file__).resolve().parent / "template_router/v2ray_up.sh",
                "down_file" : Path(__file__).resolve().parent / "template_router/v2ray_down.sh",
                "pid_file" : "/tmp/v2ray.pid",
                "log_file" : "/tmp/v2ray.log",
                "interface" : "tun0",
                "config_file" : "/tmp/v2ray.config",
                "tun2socks" : "go-tun2socks",
                "tun2socks_log_file" : "/tmp/tun2socks.log",
                "dns2socks_log_file" : "/tmp/dns2socks.log",
            },
            "check_vpn" : Path(__file__).resolve().parent / "template_router/check_vpn.sh",
        }
        self.vpn = vpn
        self.general = General.objects.first()

    def ConnectVPN(self, timeout_arg, try_count_arg):
        res = -1
        output = ""
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass

            up_file = self.VpnList["openconnect"]["up_file"]
            pid_file = "--pid_file '{}'".format(self.VpnList["openconnect"]["pid_file"])
            log_file = "--log_file '{}'".format(self.VpnList["openconnect"]["log_file"])
            timeout = "--timeout '{}'".format(timeout_arg)
            try_count = "--try_count '{}'".format(try_count_arg)

            protocol = "--protocol '{}'".format(openconnect.protocol)
            gateway = "--gateway '{}'".format(openconnect.host + ":" + str(openconnect.port))
            username = "--username '{}'".format(openconnect.username)
            password = "--password '{}'".format(openconnect.password)
            interface = "--interface '{}'".format(self.VpnList["openconnect"]["interface"])
            no_dtls = "--no_dtls" if openconnect.no_dtls else ""
            passtos = "--passtos" if openconnect.passtos else ""
            no_deflate = "--no_deflate" if openconnect.no_deflate else ""
            deflate = "--deflate" if openconnect.deflate else ""
            no_http_keepalive = "--no_http_keepalive" if openconnect.no_http_keepalive else ""
            log = "--log" if self.general.log else ""
            
            c = Execte("{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(\
                up_file, pid_file, log_file, timeout, try_count,\
                protocol, gateway, username, password, interface, no_dtls, passtos, no_deflate, deflate, no_http_keepalive,\
                log)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            
            up_file = self.VpnList["v2ray"]["up_file"]
            pid_file = "--pid_file '{}'".format(self.VpnList["v2ray"]["pid_file"])
            log_file = "--log_file '{}'".format(self.VpnList["v2ray"]["log_file"])
            timeout = "--timeout '{}'".format(timeout_arg)
            try_count = "--try_count '{}'".format(try_count_arg)

            # write config file
            config_file = self.VpnList["v2ray"]["config_file"]
            config_json = v2ray.config_json
            f = open(config_file, "w")
            f.write(config_json)
            f.close()
            #
            config = "--config '{}'".format(config_file)
            
            vpn_interface = "--vpn_interface '{}'".format(self.VpnList["v2ray"]["interface"])
            config_json = v2ray.config_json
            js = json.loads(config_json)
            v2ray_inbounds_port = "--v2ray_inbounds_port '{}'".format(js["inbounds"][0]["port"])
            v2ray_outbounds_address = "--v2ray_outbounds_address '{}'".format(js["outbounds"][0]["settings"]["vnext"][0]["address"])
            tun2socks = "--tun2socks '{}'".format(self.VpnList["v2ray"]["tun2socks"])
            tun2socks_log_file = "--tun2socks_log_file '{}'".format(self.VpnList["v2ray"]["tun2socks_log_file"])
            dns_server = "--dns_server '{}'".format(self.general.dns.split(",")[0]) if self.general.dns_Mode == self.general.DnsMode._3 and self.general.dns != "" else ""
            dns_log = "--dns_log '{}'".format(self.VpnList["v2ray"]["dns2socks_log_file"]) if self.general.dns_Mode == self.general.DnsMode._3 and self.general.dns != "" else ""
            log = "--log" if self.general.log else ""

            c = Execte("{} {} {} {} {} {} {} {} {} {} {} {} {} {}".format(\
                up_file, pid_file, log_file, timeout, try_count,\
                config,\
                vpn_interface, v2ray_inbounds_port, v2ray_outbounds_address, tun2socks, tun2socks_log_file, dns_server, dns_log,\
                log)
            )
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

        else:
            res = -1
            output = "Not Implimnet Yet"

        return res, output

    def DisconnectVPN(self):
        res = -1
        output = ""
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass

            down_file = self.VpnList["openconnect"]["down_file"]
            pid_file = "--pid_file '{}'".format(self.VpnList["openconnect"]["pid_file"])
            log_file = "--log_file '{}'".format(self.VpnList["openconnect"]["log_file"])
            log = "--log" if self.general.log else ""

            c = Execte("{} {} {} {}".format(down_file, pid_file, log_file, log))
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()
            
        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass

            down_file = self.VpnList["v2ray"]["down_file"]
            pid_file = "--pid_file '{}'".format(self.VpnList["v2ray"]["pid_file"])
            log_file = "--log_file '{}'".format(self.VpnList["v2ray"]["log_file"])
            vpn_interface = "--vpn_interface '{}'".format(self.VpnList["v2ray"]["interface"])
            config_json = v2ray.config_json
            js = json.loads(config_json)
            v2ray_outbounds_address = "--v2ray_outbounds_address '{}'".format(js["outbounds"][0]["settings"]["vnext"][0]["address"])
            badvpn_tun2socks_log_file = "--badvpn_tun2socks_log_file '{}'".format(self.VpnList["v2ray"]["badvpn-tun2socks_log_file"])
            dns_log = "--dns_log '{}'".format(self.VpnList["v2ray"]["dns2socks_log_file"]) if self.general.dns_Mode == self.general.DnsMode._3 and self.general.dns != "" else ""
            log = "--log" if self.general.log else ""

            c = Execte("{} {} {} {} {} {} {} {}".format(down_file, pid_file, log_file, vpn_interface, v2ray_outbounds_address, badvpn_tun2socks_log_file, dns_log, log))
            c.do()
            c.print()
            res = c.returncode
            output = c.getSTD()

        return res, output

    def is_running(self):
        res = False

        pid = self.read_pid_file()
        if pid != 0:
            c_proc = Execte("kill -0 {}".format(pid))
            c_proc.do()
            c_proc.print()

            check_vpn_res = False
            if c_proc.isSuccess():
                if self.general.check_vpn_method == self.general.CheckVpnMethod.disable:
                    check_vpn_res = True
                else:
                    method = self.general.check_vpn_method
                    if method == self.general.CheckVpnMethod.random:
                        method = self.general.CheckVpnMethod.curl if random.randint(1, 2) == 1 else self.general.CheckVpnMethod.ping
                    list_method = self.general.check_vpn_list_method

                    list = ()
                    timeout = None
                    retry = None
                    if method == self.general.CheckVpnMethod.curl:
                        list = self.general.check_vpn_curl_list.split()
                        timeout = self.general.check_vpn_curl_timeout
                        retry = self.general.check_vpn_curl_retry
                    elif method == self.general.CheckVpnMethod.ping:
                        list = self.general.check_vpn_ping_list.split()
                        timeout = self.general.check_vpn_ping_timeout
                        retry = self.general.check_vpn_ping_retry

                    if len(list) == 0:
                        check_vpn_res = False

                    elif list_method == self.general.CheckVpnListMethod.once:
                        check_vpn_res = False
                        for domain in list:
                            if domain != "":
                                check_vpn = self.VpnList["check_vpn"]
                                _method =  "--method '{}'".format(method)
                                _domain = "--domain '{}'".format(domain)
                                _timeout = "--timeout '{}'".format(timeout)
                                _retry = "--retry '{}'".format(retry)
                                c = Execte("{} {} {} {} {}".format(
                                    check_vpn, _method, _domain, _timeout, _retry)
                                )
                                c.do()
                                c.print()
                                if c.isSuccess():
                                    check_vpn_res = True
                                    break

                    elif list_method == self.general.CheckVpnListMethod.all:
                        check_vpn_res = True
                        for domain in list:
                            if domain != "":
                                check_vpn = self.VpnList["check_vpn"]
                                _method =  "--method '{}'".format(method)
                                _domain = "--domain '{}'".format(domain)
                                _timeout = "--timeout '{}'".format(timeout)
                                _retry = "--retry '{}'".format(retry)
                                c = Execte("{} {} {} {} {}".format(
                                    check_vpn, _method, _domain, _timeout, _retry)
                                )
                                c.do()
                                c.print()
                                if not c.isSuccess():
                                    check_vpn_res = False
                                    break

                    elif list_method == self.general.CheckVpnListMethod.random:
                        check_vpn_res = False
                        domain = list[random.randint(0, len(list) - 1)]
                        if domain != "":
                            check_vpn = self.VpnList["check_vpn"]
                            _method =  "--method '{}'".format(method)
                            _domain = "--domain '{}'".format(domain)
                            _timeout = "--timeout '{}'".format(timeout)
                            _retry = "--retry '{}'".format(retry)
                            c = Execte("{} {} {} {} {}".format(
                                check_vpn, _method, _domain, _timeout, _retry)
                            )
                            c.do()
                            c.print()
                            if c.isSuccess():
                                check_vpn_res = True

            if c_proc.isSuccess() and check_vpn_res:
                res = True

        return res

    def read_pid_file(self):
        pid = 0
        pid_file = ""
        if isinstance(self.vpn.subclass, OpenconnectConfig):
            openconnect = self.vpn.subclass
            pid_file = self.VpnList["openconnect"]["pid_file"]
        elif isinstance(self.vpn.subclass, V2rayConfig):
            v2ray = self.vpn.subclass
            pid_file = self.VpnList["v2ray"]["pid_file"]

        if pid_file != "" and os.path.isfile(pid_file):
            file = open(pid_file, "r")
            pid = file.read().strip()

        return pid
