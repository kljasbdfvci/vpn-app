# Generated by Django 4.1.1 on 2022-12-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0024_dhcpserverconfig_mac_hotspotconfig_mac_lanconfig_mac_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dhcpserverconfig',
            name='enable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='hotspotconfig',
            name='enable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lanconfig',
            name='enable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='wlanconfig',
            name='enable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='general',
            name='check_vpn_curl_list',
            field=models.CharField(blank=True, default='https://api.ipify.org?format=json\nhttp://api.ipify.org?format=json\nhttps://checkip.amazonaws.com\nhttp://checkip.amazonaws.com\nhttps://icanhazip.com\nhttp://icanhazip.com\nhttps://jsonip.com', max_length=4098),
        ),
        migrations.AlterField(
            model_name='general',
            name='check_vpn_curl_timeout',
            field=models.IntegerField(default=15),
        ),
        migrations.AlterField(
            model_name='general',
            name='check_vpn_ping_list',
            field=models.CharField(blank=True, default='8.8.8.8\n1.1.1.1\n208.67.222.222', max_length=4098),
        ),
        migrations.AlterField(
            model_name='general',
            name='check_vpn_ping_timeout',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='general',
            name='dns',
            field=models.CharField(blank=True, default='8.8.8.8\n1.1.1.1\n208.67.222.222', max_length=128),
        ),
        migrations.AlterField(
            model_name='general',
            name='v2ray_mode',
            field=models.CharField(choices=[('badvpn-tun2socks', 'badvpn-tun2socks'), ('go-tun2socks', 'go-tun2socks'), ('tun2socks', 'tun2socks')], default='badvpn-tun2socks', max_length=64),
        ),
    ]
