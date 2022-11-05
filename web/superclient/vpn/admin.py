from django.contrib import admin
from django import forms
from .models import OpenVpnConfig, OpenconnectConfig, L2tpConfig, ShadowSocksConfig, V2rayConfig, V2rayUrlConfig



@admin.register(OpenconnectConfig)
class OpenconnectConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'priority', 'success', 'failed')

#@admin.register(OpenVpnConfig)
#class OpenVpnConfigAdmin(admin.ModelAdmin):
#    list_display = ('name', 'enable', 'priority', 'success', 'failed')

#@admin.register(L2tpConfig)
#class L2tpConfigAdmin(admin.ModelAdmin):
#    list_display = ('name', 'enable', 'priority', 'success', 'failed')

#@admin.register(ShadowSocksConfig)
#class ShadowSocksConfigAdmin(admin.ModelAdmin):
#    list_display = ('name', 'enable', 'priority', 'success', 'failed')

class V2rayConfigAdminForm(forms.ModelForm):
    class Meta:
        model = V2rayConfig
        widgets = {
            'config_json': forms.Textarea,
            'config_url': forms.Textarea
        }
        fields = '__all__' 

@admin.register(V2rayConfig)
class V2rayConfigAdmin(admin.ModelAdmin):
    form = V2rayConfigAdminForm
    list_display = ('name', 'enable', 'host', 'port','priority', 'success', 'failed')
    readonly_fields = ('config_url', 'config_json')

class V2rayUrlConfigAdminForm(forms.ModelForm):
    class Meta:
        model = V2rayConfig
        widgets = {
            'config_json': forms.Textarea,
            'config_url': forms.Textarea
        }
        fields = '__all__'

@admin.register(V2rayUrlConfig)
class V2rayUrlConfigAdmin(admin.ModelAdmin):
    form = V2rayUrlConfigAdminForm
    list_display = ('name', 'enable', 'config_url', 'priority', 'success', 'failed')
    readonly_fields = ('name', 'host', 'port', 'config_json', 'v', 'protocol', 'uid', 'alter_id', 'tls', 'tls_allow_insecure', 'network', 'ws_path', 'ws_host')
