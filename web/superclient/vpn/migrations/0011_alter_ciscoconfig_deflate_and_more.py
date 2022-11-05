# Generated by Django 4.1.1 on 2022-11-03 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn', '0010_ciscoconfig_deflate_ciscoconfig_no_http_keepalive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciscoconfig',
            name='deflate',
            field=models.BooleanField(default=False, help_text='Enable all compression, including stateful modes. By default, only stateless compression algorithms are enabled.'),
        ),
        migrations.AlterField(
            model_name='ciscoconfig',
            name='no_deflate',
            field=models.BooleanField(default=False, help_text='Disable all compression.'),
        ),
        migrations.AlterField(
            model_name='ciscoconfig',
            name='no_dtls',
            field=models.BooleanField(default=False, help_text='Disable DTLS and ESP'),
        ),
        migrations.AlterField(
            model_name='ciscoconfig',
            name='no_http_keepalive',
            field=models.BooleanField(default=False, help_text='Version 8.2.2.5 of the Cisco ASA software has a bug where it will forget the client’s SSL certificate when HTTP connections are being re-used for multiple requests. So far, this has only been seen on the initial connection, where the server gives an HTTP/1.0 redirect response with an explicit Connection: Keep-Alive directive. OpenConnect as of v2.22 has an unconditional workaround for this, which is never to obey that directive after an HTTP/1.0 response.'),
        ),
        migrations.AlterField(
            model_name='ciscoconfig',
            name='passtos',
            field=models.BooleanField(default=False, help_text='Copy TOS / TCLASS of payload packet into DTLS and ESP packets. This is not set by default because it may leak information about the payload (for example, by differentiating voice/video traffic).'),
        ),
    ]