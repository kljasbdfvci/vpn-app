from django.db import models
from superclient.hotspot.models import Profile
from superclient.vpn.models import Configuration



class ServiceStatus(models.Model):

    on = models.BooleanField(default=0)

    active_profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True
    )

    active_vpn = models.OneToOneField(
        Configuration,
        on_delete=models.SET_NULL,
        null=True
    )

    @staticmethod
    def get():
        if ServiceStatus.objects.all().count() == 0:
            status = ServiceStatus.objects.create()
            status.save()

        return ServiceStatus.objects.first()

    def changeActiveProfile(self, profile):
        self.active_profile = profile
        self.save()



#     @property
#     def ap(self):
#         """
#         return access point
#         """
#         return AccessPoint(
#             interface=self.interface, ssid=self.ssid, wpa_passphrase=self.wpa_passphrase,
#             ip=self.ip, dhcp_ip_from=self.dhcp_ip_from, dhcp_ip_to=self.dhcp_ip_to, netmask=self.netmask
#         )

# # Deprecated use action.models.ServiceStatus
# class Status(models.Model):
#     active_profile = models.OneToOneField(
#         Profile,
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     @staticmethod
#     def get():
#         if Status.objects.all().count() == 0:
#             status = Status.objects.create()
#             status.save()

#         return Status.objects.first()

#     def changeActiveProfile(self, profile):
#         self.active_profile = profile
#         self.save()
