# Generated by Django 4.1.1 on 2022-11-27 12:58

from django.db import migrations, models
import django.db.models.deletion
import superclient.setting.models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0002_rename_dnsmode_setting_dns_mode'),
    ]

    operations = [
        migrations.CreateModel(
            name='DhcpServerConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface', models.CharField(max_length=16, unique=True, validators=[superclient.setting.models.validate_interface])),
                ('subnet_mask', models.CharField(default='255.255.255.0', max_length=16)),
                ('ip_address', models.CharField(default='192.168.10.1', max_length=16)),
                ('dhcp_ip_address_from', models.CharField(default='192.168.10.10', max_length=16)),
                ('dhcp_ip_address_to', models.CharField(default='192.168.10.30', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface', models.CharField(max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HotspotConfig',
            fields=[
                ('network_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='setting.network')),
                ('ssid', models.CharField(max_length=128)),
                ('wpa_passphrase', models.CharField(max_length=128)),
                ('channel', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14')], default='6', max_length=8)),
            ],
            bases=('setting.network',),
        ),
        migrations.CreateModel(
            name='LanConfig',
            fields=[
                ('network_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='setting.network')),
                ('dhcp', models.BooleanField(default=True)),
                ('ip_address_1', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_1', models.CharField(blank=True, max_length=16)),
                ('ip_address_2', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_2', models.CharField(blank=True, max_length=16)),
                ('ip_address_3', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_3', models.CharField(blank=True, max_length=16)),
                ('ip_address_4', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_4', models.CharField(blank=True, max_length=16)),
            ],
            bases=('setting.network',),
        ),
        migrations.CreateModel(
            name='WlanConfig',
            fields=[
                ('network_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='setting.network')),
                ('ssid', models.CharField(max_length=128)),
                ('wpa_passphrase', models.CharField(max_length=128)),
                ('dhcp', models.BooleanField(default=True)),
                ('ip_address_1', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_1', models.CharField(blank=True, max_length=16)),
                ('ip_address_2', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_2', models.CharField(blank=True, max_length=16)),
                ('ip_address_3', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_3', models.CharField(blank=True, max_length=16)),
                ('ip_address_4', models.CharField(blank=True, max_length=16)),
                ('subnet_mask_4', models.CharField(blank=True, max_length=16)),
            ],
            bases=('setting.network',),
        ),
    ]