from django.shortcuts import render
from pathlib import Path
from superclient.hotspot.models import Profile
from .models import ServiceStatus as Status
from .service.Execte import *



def index(request):
    status = Status.get()
    active_profile = status.active_profile

    isOn = status.on

    if request.method == 'POST':
        print('HERE I AM')
        if isOn:
            print('az ghabl onam mikham off sham')
            status.active_profile = None
            status.on = False
            status.save()
        else:
            print('on nistam mikham besham')
            selected_profile = Profile.objects.filter(name=request.POST.dict()['profile']).first()
            active_profile = selected_profile
            status.active_profile = active_profile
            status.on = True
            status.save()

    submitText = 'Off' if isOn else 'On'
    profiles = list(Profile.objects.values_list('name', flat=True))
  
    context = {
        'isOn': isOn, 
        'profiles': profiles, 
        'submitText': submitText, 
        'activeProfile': '' if active_profile is None else active_profile.name
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
