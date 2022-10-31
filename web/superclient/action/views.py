from django.shortcuts import render
from pathlib import Path
from superclient.hotspot.models import Profile
from .models import ServiceStatus as Status
from .service.Execte import *



def index(request):
    status = Status.get()

    if request.method == 'POST':
        if not status.on:
            selected_profile = Profile.objects.filter(name=request.POST.dict()['profile']).first()
            status.change_active_profile(selected_profile)
        
        status.toggle_on()

    submitText = 'Off' if status.on else 'On'
    profiles = list(Profile.objects.values_list('name', flat=True))
  
    context = {
        'isOn': status.on, 
        'profiles': profiles, 
        'submitText': submitText, 
        'activeProfile': '' if status.active_profile is None else status.active_profile.name,
        'activeProfileSSID': '' if status.active_profile is None else status.active_profile.ssid,
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
