from django.db import models
from superclient.action.service.AccessPoint import AccessPoint


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1028, blank=True)
    interface = models.CharField(max_length=128)
    class Channel(models.TextChoices):
        _1 = "1", "1"
        _2 = "2", "2"
        _3 = "3", "3"
        _4 = "4", "4"
        _5 = "5", "5"
        _6 = "6", "6"
        _7 = "7", "7"
        _8 = "8", "8"
        _9 = "9", "9"
        _10 = "10", "10"
        _11 = "11", "11"
        _12 = "12", "12"
        _13 = "13", "13"
        _14 = "14", "14"
    channel = models.CharField(max_length=8, choices=Channel.choices, default=Channel._6)
    ssid = models.CharField(max_length=128)
    wpa_passphrase = models.CharField(max_length=128)
    ip = models.CharField(max_length=16, default='192.168.10.1')
    dhcp_ip_from = models.CharField(max_length=16, default='192.168.10.10')
    dhcp_ip_to = models.CharField(max_length=16, default='192.168.10.30')
    netmask = models.CharField(max_length=20, default='255.255.255.0')
    dns = models.CharField(max_length=128, default='1.1.1.1,8.8.8.8,208.67.222.222', blank=True)

    @property
    def access_point(self):
        return AccessPoint(
            interface=self.interface, channel=self.channel, ssid=self.ssid, wpa_passphrase=self.wpa_passphrase,
            ip=self.ip, dhcp_ip_from=self.dhcp_ip_from, dhcp_ip_to=self.dhcp_ip_to, netmask=self.netmask, dns=self.dns
        )
