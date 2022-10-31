from django.contrib import admin
from .models import OpenVpnConfig, CiscoConfig, L2tpConfig, ShadowSocksConfig


admin.site.register(OpenVpnConfig)
admin.site.register(CiscoConfig)
admin.site.register(L2tpConfig)
admin.site.register(ShadowSocksConfig)
