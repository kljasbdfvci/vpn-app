# Generated by Django 4.1.1 on 2022-12-07 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0009_general_check_vpn_curl_domain_list_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='general',
            name='check_vpn_curl_domain_list',
        ),
        migrations.AddField(
            model_name='general',
            name='check_vpn_curl_list',
            field=models.CharField(blank=True, default='https://api.ipify.org?format=json\nhttps://checkip.amazonaws.com\nhttps://icanhazip.com\nhttps://jsonip.com', max_length=4098),
        ),
        migrations.AddField(
            model_name='general',
            name='check_vpn_list_method',
            field=models.CharField(choices=[('once', 'Once from all list successful'), ('all', 'All from list successful'), ('random', 'Once randomly successful from list')], default='random', max_length=64),
        ),
        migrations.AddField(
            model_name='general',
            name='check_vpn_method',
            field=models.CharField(choices=[('disable', 'Disable'), ('curl', 'Curl'), ('ping', 'Ping'), ('random', 'Curl or Ping randomly')], default='random', max_length=64),
        ),
        migrations.AddField(
            model_name='general',
            name='check_vpn_ping_list',
            field=models.CharField(blank=True, default='1.1.1.1\n8.8.8.8\n208.67.222.222', max_length=4098),
        ),
        migrations.AddField(
            model_name='general',
            name='check_vpn_ping_retry',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='general',
            name='check_vpn_ping_timeout',
            field=models.IntegerField(default=3),
        ),
    ]
