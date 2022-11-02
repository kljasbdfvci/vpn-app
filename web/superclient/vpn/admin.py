from django.contrib import admin
from .models import OpenVpnConfig, CiscoConfig, L2tpConfig, ShadowSocksConfig



@admin.register(OpenVpnConfig)
class OpenVpnConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'priority', 'success', 'failed')

@admin.register(CiscoConfig)
class CiscoConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'priority', 'success', 'failed')

@admin.register(L2tpConfig)
class L2tpConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'priority', 'success', 'failed')

@admin.register(ShadowSocksConfig)
class ShadowSocksConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'priority', 'success', 'failed')