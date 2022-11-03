from django.db import models


# Create your models here.
class Configuration(models.Model):

    name = models.CharField(max_length=256, unique=True)  
    description = models.CharField(max_length=1028, blank=True)
    enable = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    success = models.IntegerField(default=0, editable=False)
    failed = models.IntegerField(default=0, editable=False)

    # Common Configuration Parameters
    host = models.CharField(max_length=128)
    port = models.IntegerField()

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

    @property
    def type(self):
        return type(self.subclass).__name__.lower().replace('config', '')

    @property
    def title(self):
        return f'{self.name} ({self.type})'


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
    protocol = models.CharField(max_length=128, choices=Protocol.choices, default=Protocol.anyconnect)
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # TODO: save encrypted password
    no_dtls = models.BooleanField(default=False, help_text="Disable DTLS and ESP")
    passtos = models.BooleanField(default=False, help_text="Copy TOS / TCLASS of payload packet into DTLS and ESP packets. This is not set by default because it may leak information about the payload (for example, by differentiating voice/video traffic).")
    no_deflate = models.BooleanField(default=False, help_text="Disable all compression.")
    deflate = models.BooleanField(default=False, help_text="Enable all compression, including stateful modes. By default, only stateless compression algorithms are enabled.")
    no_http_keepalive = models.BooleanField(default=False, help_text="Version 8.2.2.5 of the Cisco ASA software has a bug where it will forget the client’s SSL certificate when HTTP connections are being re-used for multiple requests. So far, this has only been seen on the initial connection, where the server gives an HTTP/1.0 redirect response with an explicit Connection: Keep-Alive directive. OpenConnect as of v2.22 has an unconditional workaround for this, which is never to obey that directive after an HTTP/1.0 response.")


class ShadowSocksConfig(Configuration):

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