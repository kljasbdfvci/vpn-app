from pathlib import Path
import string
from sys import stdout
import nmcli
from ...vpn.models import *
import os.path

# local
from .Execte import *

class Router:
    def __init__(self,vpn : Configuration):
        self.VpnList = {
            "anyconnect": {
                "up_file" : Path(__file__).resolve().parent / "template/up_aynconnect.sh",
                "pid_file" : Path(__file__).resolve().parent / "anyconnect.pid",
                "interface" : "tun0"
            },
        }
        self.vpn = vpn

    def ConnectVPN(self, timeout):
        res = -1
        output = ""
        if isinstance(self.vpn, CiscoConfig):
            up_file = self.VpnList["anyconnect"]["up_file"]
            gateway = self.vpn.host + ":" + str(self.vpn.port)
            username = self.vpn.username
            password = self.vpn.password
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            interface = self.VpnList["anyconnect"]["interface"]
            c1 = Execte("{} {} {} {} {} {} {}".format(up_file, gateway, username, password, timeout, pid_file, interface))
            c1.do()
            res = c1.returncode
            output = c1.stdout + c1.stderr
        else:
            res = -1
            output = "Not Implimnet Yet"

        if res == 0:
            self._ip_table()

        return res, output

    def DisconnectVPN(self):
        res = -1
        output = ""
        if isinstance(self.vpn, CiscoConfig):
            pid_file = self.VpnList["anyconnect"]["pid_file"]
            if os.path.isfile(pid_file):
                c1 = Execte("(kill -SIGINT `cat {}` && rm {}) || (kill -SIGKILL `cat {}` && rm {})".format(pid_file, pid_file, pid_file, pid_file))
                c1.do()
                res = c1.returncode
                output = c1.stdout + c1.stderr
            else:
                res = 0
                output = "vpn is already disable."

        else:
            res = -1
            output = "Not Implimnet Yet"

        return res, output

    def _ip_table(self):
        # sysctl -w net.ipv4.ip_forward=1
        # iptables -t nat -A  POSTROUTING -o tun0 -j MASQUERADE
        if isinstance(self.vpn, CiscoConfig):
            interface = self.VpnList["anyconnect"]["interface"]
            c1 = Execte("sysctl -w net.ipv4.ip_forward=1")
            c1.do()
            c1 = Execte("iptables -t nat -A  POSTROUTING -o {} -j MASQUERADE".format(interface))
            c1.do()
        else:
            res = -1
            output = "Not Implimnet Yet"



















class Router1:
    def __init__(self):
        self.VpnProtocolList = {
            "anyconnect": {
                "run_script" : "./template/up_aynconnect.sh",
            },
        }
        self.VPNList = []

    def AddVPN(self, id, protocol, cfg):
        
        if protocol == "anyconnect":
            gateway = cfg["gateway"]
            username = cfg["username"]
            password = cfg["password"]
            priority = cfg["priority"]
            full_cfg = {
                "vpn.service-type" : "openconnect",
                "vpn.data" : '''
authtype=password, 
autoconnect-flags=2, 
certsigs-flags=2, 
cookie-flags=2, 
enable_csd_trojan=no, 
gateway={}, 
gateway-flags=2, 
gwcert-flags=2, 
lasthost-flags=2, 
pem_passphrase_fsid=yes, 
prevent_invalid_cert=no, 
protocol=anyconnect, 
resolve-flags=2, 
stoken_source=disabled, 
xmlconfig-flags=2, 
service-type=openconnect,
username={}, 
password={}, 
priority={}, 
success=0, 
failed=0
'''.format(gateway, username, password, priority),
"vpn.secrets" : '''
'''.format(),
"ipv4.method" : "auto",
"ipv6.method" : "auto"
            }
            nmcli.connection.add("vpn", full_cfg, "*", id, False)
        else:
            pass

    def DeleteVPN(self, id):
        nmcli.connection.delete(id)

    def GetVPNData(self, id, cfg):
        if "vpn.data." in cfg:
            list = nmcli.connection.show(id)["vpn.data"].split(",")
            vpndataitem = cfg[9:]
            for x in list:
                key = x.split("=")[0].strip()
                value = x.split("=")[1].strip()
                if key == vpndataitem:
                    return value
        else:
            return nmcli.connection.show(id)[cfg]

    def SetVPNData(self, id, cfg, data):
        if "vpn.data." in cfg:
            list = nmcli.connection.show(id)["vpn.data"].split(",")
            vpndataitem = cfg[9:]
            for x in list:
                key = x.split("=")[0].strip()
                if key == vpndataitem:
                    list.remove(x)
                    list.append("{}={}".format(vpndataitem, data))
                    break
            nmcli.connection.modify(id, {"vpn.data" : ", ".join(list)})
        else:
            nmcli.connection.modify(id, {cfg : data})
    
    def _updateFailedSuccess(self, id, res):
        if res != 0:
            failed = int(self.GetVPNData(id, "vpn.data.failed")) + 1
            self.SetVPNData(id, "vpn.data.failed", failed)
        else:
            success = int(self.GetVPNData(id, "vpn.data.success")) + 1
            self.SetVPNData(id, "vpn.data.failed", success)

    def ConnectVPN(self, id):
        protocol = self.GetVPNData(id, "vpn.data.protocol")
        res = -1
        output = ""
        if protocol == "anyconnect":
            run_script = self.VpnProtocolList["anyconnect"]["run_script"]
            username = self.GetVPNData(id, "vpn.data.username")
            password = self.GetVPNData(id, "vpn.data.password")
            c1 = Execte("{} {} {} {}".format(run_script, id, username, password))
            c1.do()
            
            list = c1.stdout.split('\n')
            if len(list) > 20:
                list = list[-20:]
            output = "\n".join(list)
            
            if "Error: Connection activation failed:" in output:
                res = -1
            else:
                res = 0
            
        else:
            res = -1
            output = "Not Implimnet Yet"

        self._updateFailedSuccess(id, res)
        return res, output

    def LoadVPN(self):
        list = nmcli.connection()
        for x in list:
            if (x.conn_type == "vpn" or x.conn_type == "tun") and x.name not in self.VPNList:
                self.VPNList.append(x.name)
