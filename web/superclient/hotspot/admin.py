from django.contrib import admin
from django import forms
from .models import Profile
from .service.hotspot import get_network_interfaces as interfaces

class ProfileAdminForm(forms.ModelForm):
    interface = forms.ChoiceField(choices=tuple((key, key) for key in interfaces()))

    class Meta:
        model = Profile
        fields = '__all__'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('name', 'interface', 'ssid')