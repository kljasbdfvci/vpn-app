from django.contrib import admin
from django import forms
from .models import OpenVpnConfig, OpenconnectConfig, L2tpConfig, ShadowSocksConfig, V2rayConfig



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

class V2rayConfigAdmin(admin.ModelAdmin):
    form = V2rayConfigAdminForm
    list_display = ('name', 'enable', 'priority', 'success', 'failed')

admin.site.register(V2rayConfig, V2rayConfigAdmin)