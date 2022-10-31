from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1028, blank=True)
    ssid = models.CharField(max_length=128)
    interface = models.CharField(max_length=128)
    wpa_passphrase = models.CharField(max_length=128)
    ip = models.CharField(max_length=16, default='192.168.10.1')
    dhcp_ip_from = models.CharField(max_length=16, default='192.168.10.10')
    dhcp_ip_to = models.CharField(max_length=16, default='192.168.10.30')
    netmask = models.CharField(max_length=20, default='255.255.255.0')
