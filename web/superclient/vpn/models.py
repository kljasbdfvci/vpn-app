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
        if(hasattr(self, 'ciscoconfig')):
            return self.ciscoconfig
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


class CiscoConfig(Configuration):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # TODO: save encrypted password
    no_dtls = models.BooleanField(default=False)
    passtos = models.BooleanField(default=False)
    no_deflate = models.BooleanField(default=False)


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