from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import base64
import json
from superclient.vpn.service.vmess2json import generate



class Configuration(models.Model):

    name = models.CharField(max_length=256, unique=True)  
    description = models.CharField(max_length=1028, blank=True)
    enable = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    success = models.IntegerField(default=0, editable=False)
    failed = models.IntegerField(default=0, editable=False)
    last_log = models.CharField(max_length=4098, blank=True)

    @property
    def subclass(self):
        if(hasattr(self, 'openconnectconfig')):
            return self.openconnectconfig
        if(hasattr(self, 'l2tpconfig')):
            return self.l2tpconfig
        if(hasattr(self, 'openvpnconfig')):
            return self.openvpnconfig
        if(hasattr(self, 'shadowsocksconfig')):
            return self.shadowsocksconfig
        if(hasattr(self, 'v2rayconfig')):
            return self.v2rayconfig

    @property
    def type(self):
        return type(self.subclass).__name__.lower().replace('config', '')

    @property
    def title(self):
        return f'{self.name} ({self.type})'

    def increase_failed(self):
        self.failed = self.failed + 1
        self.save()

    def increase_success(self):
        self.success = self.success + 1
        self.save()
    
    def add_log(self, log):
        self.last_log = log
        self.save()


class L2tpConfig(Configuration):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # TODO: save encrypted password


class OpenconnectConfig(Configuration):

    class Protocol(models.TextChoices):
        anyconnect = "anyconnect", "Cisco (AnyConnect)"
        nc = "nc", "Juniper Network Connect"
        gp = "gp", "Palo Alto Networks (PAN) GlobalProtect VPN"
        pulse = "pulse", "Junos Pulse VPN"
        f5 = "f5", "F5 Big-IP VPN"
        fortinet = "fortinet", "Fortinet Fortigate VPN"
        array = "array", "Array Networks SSL VPN"
    
    host = models.CharField(max_length=128)
    port = models.IntegerField()
    protocol = models.CharField(max_length=128, choices=Protocol.choices, default=Protocol.anyconnect)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # TODO: save encrypted password
    no_dtls = models.BooleanField(default=False, help_text="Disable DTLS and ESP")
    passtos = models.BooleanField(default=False, help_text="Copy TOS / TCLASS of payload packet into DTLS and ESP packets. This is not set by default because it may leak information about the payload (for example, by differentiating voice/video traffic).")
    no_deflate = models.BooleanField(default=False, help_text="Disable all compression.")
    deflate = models.BooleanField(default=False, help_text="Enable all compression, including stateful modes. By default, only stateless compression algorithms are enabled.")
    no_http_keepalive = models.BooleanField(default=False, help_text="Version 8.2.2.5 of the Cisco ASA software has a bug where it will forget the client’s SSL certificate when HTTP connections are being re-used for multiple requests. So far, this has only been seen on the initial connection, where the server gives an HTTP/1.0 redirect response with an explicit Connection: Keep-Alive directive. OpenConnect as of v2.22 has an unconditional workaround for this, which is never to obey that directive after an HTTP/1.0 response.")


class ShadowSocksConfig(Configuration):

    host = models.CharField(max_length=128)
    port = models.IntegerField()
    password = models.CharField(max_length=128)  # TODO: save encrypted password

    class Encryption(models.TextChoices):
        chacha20_ietf_poly = "chacha20poly", "chacha20-ietf-poly1305"
        aes_256_gcm = "256gcm", "aes-256-gcm"
        aes_256_ctr = "256ctr", "aes-256-ctr"
        aes_256_cfb = "256cfb", "aes-256-cfb"

    encryption = models.CharField(max_length=12, choices=Encryption.choices)


class OpenVpnConfig(Configuration):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # TODO: save encrypted password


class V2rayConfig(Configuration):

    class Protocol(models.TextChoices):
        vmess = "vmess", "VMESS"
        vless = "vless", "VLESS"  # we dont have alter_id in vless

    class Network(models.TextChoices):
        vmess = "tpc", "TCP"
        vless = "ws", "WebSocket"

    class Tls(models.TextChoices):
        tls = "tls", "TLS"
        off = "off", "OFF"

    host = models.CharField(max_length=128, blank=True)
    port = models.IntegerField(null=True)
    v = models.CharField(max_length=8, default='2')
    protocol = models.CharField(max_length=8, choices=Protocol.choices)
    uid = models.CharField(max_length=64, blank=True)
    alter_id = models.CharField(max_length=64, blank=True)
    tls = models.CharField(max_length=8, choices=Tls.choices, blank=True)
    tls_allow_insecure = models.BooleanField(default=False)
    network = models.CharField(max_length=8, choices=Network.choices, blank=True)
    ws_path = models.CharField(max_length=512, blank=True)
    ws_host = models.CharField(max_length=256, blank=True)
    config_url = models.CharField(max_length=2048, blank=True)
    config_json = models.CharField(max_length=4098, blank=True)

    config_type = 'property'

    def save(self, *args, **kwargs):
        if self.config_type == 'url':
            conf = self.config_url.split('://')
            config = json.loads(base64.b64decode(conf[1].encode("utf-8")))
            self.v = config.get('v')
            self.name = config.get('ps')
            self.host = config.get('add')
            self.port = config.get('port')
            self.protocol = conf[0]
            self.uid = config.get('id')
            self.alter_id = config.get('aid')
            self.network = config.get('net')
            self.ws_path = config.get('path')
            self.ws_host = config.get('host')
            self.tls = config.get('tls')
        
        elif self.config_type == 'property':
            configjson = {
                "v": self.v,
                "ps": self.name,
                "add": self.host,
                "port": str(self.port),
                "id": self.uid,
                "aid": self.alter_id,
                "net": self.network,
                "type": 'none',
                "host": self.ws_host,
                "path": self.ws_path,
                "tls": self.tls,
            }

            encoded_config = base64.b64encode(json.dumps(configjson, sort_keys=True).encode('utf-8')).decode()
            self.config_url = f'{self.protocol}://{encoded_config}'

        self.config_json = generate(self.config_url)   

        super(V2rayConfig, self).save(*args, **kwargs)


class V2rayUrlConfig(V2rayConfig):
    class Meta:
        proxy = True

    config_type = 'url'
