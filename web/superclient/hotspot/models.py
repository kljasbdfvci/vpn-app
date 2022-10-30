from dataclasses import field
from enum import unique
from pyexpat import model
from statistics import mode
from django.db import models
from superclient.service.AccessPoint import AccessPoint



class Profile(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1028)
    ssid = models.CharField(max_length=128)
    interface = models.CharField(max_length=128)
    wpa_passphrase = models.CharField(max_length=128)
    ip = models.CharField(max_length=16, default='192.168.10.1')
    dhcp_ip_from = models.CharField(max_length=16, default='192.168.10.10')
    dhcp_ip_to = models.CharField(max_length=16, default='192.168.10.30')
    netmask = models.CharField(max_length=20, default='255.255.255.0')

    @property
    def ap(self):
        """
        return access point
        """
        return AccessPoint(
            interface=self.interface, ssid=self.ssid, wpa_passphrase=self.wpa_passphrase,
            ip=self.ip, dhcp_ip_from=self.dhcp_ip_from, dhcp_ip_to=self.dhcp_ip_to, netmask=self.netmask
        )

# Deprecated use action.models.ServiceStatus
class Status(models.Model):
    active_profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True
    )

    @staticmethod
    def get():
        if Status.objects.all().count() == 0:
            status = Status.objects.create()
            status.save()

        return Status.objects.first()

    def changeActiveProfile(self, profile):
        self.active_profile = profile
        self.save()
