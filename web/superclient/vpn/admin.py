from django.contrib import admin
from django import forms
from .models import OpenVpnConfig, OpenconnectConfig, L2tpConfig, ShadowSocksConfig, V2rayConfig, V2rayUrlConfig
from ..action.models import ServiceStatus

class OpenconnectConfigAdminForm(forms.ModelForm):
    class Meta:
        model = OpenconnectConfig
        widgets = {
            'last_log': forms.Textarea,
        }
        fields = '__all__' 

@admin.register(OpenconnectConfig)
class OpenconnectConfigAdmin(admin.ModelAdmin):
    form = OpenconnectConfigAdminForm
    list_display = ['name', 'enable', 'priority', 'success', 'failed', 'host', 'port']
    readonly_fields = ['last_log']

    def get_fields (self, request, obj=None, **kwargs):
        fields = super().get_fields(request, obj, **kwargs)
        configuration_list = ['name', 'description', 'enable', 'priority', 'last_log']
        for i in range(len(configuration_list)): 
            fields.remove(configuration_list[i])
            fields.insert(i, configuration_list[i])
        return fields

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
            'last_log': forms.Textarea,
            'config_json': forms.Textarea,
            'config_url': forms.Textarea
        }
        fields = '__all__' 

@admin.register(V2rayConfig)
class V2rayConfigAdmin(admin.ModelAdmin):
    form = V2rayConfigAdminForm
    list_display = ['name', 'enable', 'priority', 'success', 'failed', 'host', 'port']
    readonly_fields = ['last_log', 'config_url', 'config_json']

    def get_fields (self, request, obj=None, **kwargs):
        fields = super().get_fields(request, obj, **kwargs)
        configuration_list = ['name', 'description', 'enable', 'priority', 'last_log']
        for i in range(len(configuration_list)): 
            fields.remove(configuration_list[i])
            fields.insert(i, configuration_list[i])
        return fields

class V2rayUrlConfigAdminForm(forms.ModelForm):
    class Meta:
        model = V2rayConfig
        widgets = {
            'last_log': forms.Textarea,
            'config_json': forms.Textarea,
            'config_url': forms.Textarea
        }
        fields = '__all__'

@admin.register(V2rayUrlConfig)
class V2rayUrlConfigAdmin(admin.ModelAdmin):
    form = V2rayUrlConfigAdminForm
    list_display = ['name', 'enable', 'priority', 'success', 'failed', 'config_url']
    readonly_fields = ['last_log', 'name', 'host', 'port', 'config_json', 'v', 'protocol', 'uid', 'alter_id', 'tls', 'tls_allow_insecure', 'network', 'ws_path', 'ws_host', 'ws_sni']

    def get_fields (self, request, obj=None, **kwargs):
        fields = super().get_fields(request, obj, **kwargs)
        configuration_list = ['name', 'description', 'enable', 'priority', 'last_log']
        for i in range(len(configuration_list)): 
            fields.remove(configuration_list[i])
            fields.insert(i, configuration_list[i])
        return fields
