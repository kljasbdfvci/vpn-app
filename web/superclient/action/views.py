from django.shortcuts import render
from pathlib import Path
from superclient.hotspot.models import Profile
from superclient.vpn.models import Configuration
from .models import ServiceStatus as Status
from .service.Execte import *
from superclient.action.task import service_checker



def index(request):
    status = Status.get()

    if request.method == 'POST':
        if not status.on:
            selected_profile = Profile.objects.filter(name=request.POST.dict()['profile']).first()
            status.change_active_profile(selected_profile)

            selected_vpn = Configuration.objects.filter(id=request.POST.dict()['vpn']).first()
            status.change_active_vpn(selected_vpn)
        
        status.toggle_on()
        service_checker(repeat=5)

    submitText = 'Off' if status.on else 'On'
    profiles = list(Profile.objects.values_list('name', flat=True))
    vpn_configs = Configuration.objects.filter(enable=True).order_by('priority').all()
    vpns = [
        {
            'title': vpn.title,
            'id': vpn.id
        }
        for vpn in vpn_configs
    ]
    vpns.insert(0, {'title': 'auto (smart)', 'id': -1})


    context = {
        'isOn': status.on, 
        'profiles': profiles, 
        'vpns': vpns,
        'submitText': submitText, 
        'activeProfile': '' if status.active_profile is None else status.active_profile.name,
        'activeProfileSSID': '' if status.active_profile is None else status.active_profile.ssid,
        'activeVpn': 'auto (smart)' if status.active_vpn is None else status.active_vpn.title,
    }
    
    return render(request, 'index.html', context)


def update(request):
    
    #
    app_version_path= Path(__file__).resolve().parent.parent.parent.parent / "version"
    file = open(app_version_path, "r")
    current_app_version = file.read().strip()
    
    #
    c = Execte("serial -r /disk/username /disk/name")
    c.do()
    available_app_version = c.stdout.strip()

    #
    can_update = False
    if current_app_version != available_app_version:
        can_update = True

    #
    updating = 0
    if request.method == 'POST':
        c = Execte("serial -u /disk/username /disk/name /disk/firmware /memory/version /tmp", False)
        c.do()
        if c.returncode == 0:
            c1 = Execte("sleep 5 && reboot &", True)
            c1.do()
            updating = 1
        else:
            updating = -1

    context = {
        'current_app_version' : current_app_version,
        'available_app_version' : available_app_version,
        'can_update' : can_update,
        'updating' : updating
    }
    return render(request, 'update.html', context)
