from django.contrib import admin
from django import forms
from .models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    #form = ProfileAdminForm
    #list_display = ('name', 'interface', 'ssid')
    class Meta:
        model = Setting
        fields = '__all__'
    def has_add_permission(self, request):
        base_add_permission = super(SettingAdmin, self).has_add_permission(request)
        if base_add_permission:
            # if there's already an entry, do not allow adding
            count = Setting.objects.all().count()
            if count == 0:
                return True
        return False