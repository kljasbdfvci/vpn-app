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

class L2tpConfig(Configuration):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # TODO: save encrypted password


class CiscoConfig(Configuration):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)  # TODO: save encrypted password


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
 
