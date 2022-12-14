from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class General(models.Model):

    class VpnSmartMode(models.TextChoices):
        success_chance = "success_chance", "Success Chance"
        priority = "priority", "Priority"
        circular = "circular", "Circular"        
    vpn_smart_mode = models.CharField(max_length=64, choices=VpnSmartMode.choices, default=VpnSmartMode.success_chance)
    class DnsMode(models.TextChoices):
        _1 = "1", "Do Nothing"
        _2 = "2", "Handle in system"
        _3 = "3", "Handle with socks (only for v2ray)"        
    dns_Mode = models.CharField(max_length=8, choices=DnsMode.choices, default=DnsMode._2)
    dns = models.CharField(max_length=128, default='1.1.1.1\n8.8.8.8\n208.67.222.222', blank=True)
    log = models.BooleanField(default=False)
    class CheckVpnMethod(models.TextChoices):
        disable = "disable", "Disable"
        curl = "curl", "Curl"
        ping = "ping", "Ping"
        random = "random", "Curl or Ping randomly"
    check_vpn_method = models.CharField(max_length=64, choices=CheckVpnMethod.choices, default=CheckVpnMethod.random)
    class CheckVpnListMethod(models.TextChoices):
        once = "once", "Once from all list successful"
        all = "all", "All from list successful"
        random = "random", "Once randomly successful from list"
    check_vpn_list_method = models.CharField(max_length=64, choices=CheckVpnListMethod.choices, default=CheckVpnListMethod.once)
    check_vpn_curl_list = models.CharField(max_length=4098, default='https://api.ipify.org?format=json\nhttps://checkip.amazonaws.com\nhttps://icanhazip.com\nhttps://jsonip.com', blank=True)
    check_vpn_curl_timeout = models.IntegerField(default=8)
    check_vpn_curl_retry = models.IntegerField(default=2)
    check_vpn_ping_list = models.CharField(max_length=4098, default='1.1.1.1\n8.8.8.8\n208.67.222.222', blank=True)
    check_vpn_ping_timeout = models.IntegerField(default=3)
    check_vpn_ping_retry = models.IntegerField(default=3)
    class V2rayMode(models.TextChoices):
        badvpn_tun2socks = "badvpn-tun2socks", "badvpn-tun2socks"
        go_tun2socks = "go-tun2socks", "go-tun2socks"
        tun2socks = "tun2socks", "tun2socks"
    v2ray_mode = models.CharField(max_length=64, choices=V2rayMode.choices, default=V2rayMode.tun2socks)

    def save(self, *args, **kwargs):
        #self.dns = "".join(self.dns.split())
        super(General, self).save(*args, **kwargs)

def LanConfig_validate_interface(value):
    if DhcpServerConfig.objects.filter(interface = value).count() != 0:
        raise ValidationError(
            _("Network interface '%s' already exists in 'Dhcp server configs'."),
            params=(value),
        )

class LanConfig(models.Model):
    interface = models.CharField(max_length=16, unique=True, validators=[LanConfig_validate_interface])
    dhcp = models.BooleanField(default=True)
    ip_address_1 = models.CharField(max_length=16, blank=True)
    subnet_mask_1 = models.CharField(max_length=16, blank=True)
    ip_address_2 = models.CharField(max_length=16, blank=True)
    subnet_mask_2 = models.CharField(max_length=16, blank=True)
    ip_address_3 = models.CharField(max_length=16, blank=True)
    subnet_mask_3 = models.CharField(max_length=16, blank=True)
    ip_address_4 = models.CharField(max_length=16, blank=True)
    subnet_mask_4 = models.CharField(max_length=16, blank=True)

def WlanConfig_validate_interface(value):
    if HotspotConfig.objects.filter(interface = value).count() != 0:
        raise ValidationError(
            _("Network interface '%s' already exists in 'Hotspot configs'."),
            params=(value),
        )
    elif DhcpServerConfig.objects.filter(interface = value).count() != 0:
        raise ValidationError(
            _("Network interface '%s' already exists in 'Dhcp server configs'."),
            params=(value),
        )
    

class WlanConfig(models.Model):
    interface = models.CharField(max_length=16, unique=True, validators=[WlanConfig_validate_interface])
    ssid = models.CharField(max_length=128)
    wpa_passphrase = models.CharField(max_length=128)
    class Driver(models.TextChoices):
        nl80211 = "nl80211", "nl80211"
        wext = "wext", "wext"
        all = "nl80211,wext", "nl80211,wext"
    driver = models.CharField(max_length=128, choices=Driver.choices, default=Driver.all)
    dhcp = models.BooleanField(default=True)
    ip_address_1 = models.CharField(max_length=16, blank=True)
    subnet_mask_1 = models.CharField(max_length=16, blank=True)
    ip_address_2 = models.CharField(max_length=16, blank=True)
    subnet_mask_2 = models.CharField(max_length=16, blank=True)
    ip_address_3 = models.CharField(max_length=16, blank=True)
    subnet_mask_3 = models.CharField(max_length=16, blank=True)
    ip_address_4 = models.CharField(max_length=16, blank=True)
    subnet_mask_4 = models.CharField(max_length=16, blank=True)

def HotspotConfig_validate_interface(value):
    if WlanConfig.objects.filter(interface = value).count() != 0:
        raise ValidationError(
            _("Network interface '%s' already exists in 'Wlan configs'."),
            params=(value),
        )

class HotspotConfig(models.Model):
    interface = models.CharField(max_length=16, unique=True, validators=[HotspotConfig_validate_interface])
    ssid = models.CharField(max_length=128)
    wpa_passphrase = models.CharField(max_length=128, blank=True)
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
    country_code = models.CharField(max_length=8, default="IR")
    class MAC_Address_Filter_Mode(models.TextChoices):
        disable = "disable", "Disable"
        block = "block", "Block"
        allow = "accept", "Allow"
    mac_address_filter_mode = models.CharField(max_length=32, choices=MAC_Address_Filter_Mode.choices, default=MAC_Address_Filter_Mode.disable)
    mac_address_filter_list = models.CharField(max_length=4098, blank=True)
    

def DhcpServerConfig_validate_interface(value):
    if LanConfig.objects.filter(interface = value).count() != 0:
        raise ValidationError(
            _("Network interface '%s' already exists in 'Lan configs'."),
            params=(value),
        )
    elif WlanConfig.objects.filter(interface = value).count() != 0:
        raise ValidationError(
            _("Network interface '%s' already exists in 'Wlan configs'."),
            params=(value),
        )
    

class DhcpServerConfig(models.Model):
    class DhcpModule(models.TextChoices):
        dnsmasq = "dnsmasq", "dnsmasq"
        dhcpd = "isc-dhcp-server", "isc-dhcp-server"
    dhcp_module = models.CharField(max_length=32, choices=DhcpModule.choices, default=DhcpModule.dnsmasq)
    interface = models.CharField(max_length=16, unique=True, validators=[DhcpServerConfig_validate_interface])
    ip_address = models.CharField(max_length=16, default='192.168.10.1')
    subnet_mask = models.CharField(max_length=16, default='255.255.255.0')
    dhcp_ip_address_from = models.CharField(max_length=16, default='192.168.10.10')
    dhcp_ip_address_to = models.CharField(max_length=16, default='192.168.10.30')
