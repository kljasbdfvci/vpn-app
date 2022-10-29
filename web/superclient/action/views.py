from django.shortcuts import render

# Create your views here.
from pathlib import Path
from superclient.hotspot.models import Profile, Status
from superclient.service.Execte import *


def index(request):
    status = Status.get()
    active_profile = status.active_profile
    isOn = False if active_profile is None else active_profile.ap.is_running() 

    if request.method == 'POST':
        if isOn:
            isOn = not active_profile.ap.stop()
            status.changeActiveProfile(None)
            status.save()
        else:
            selected_profile = Profile.objects.filter(name=request.POST.dict()['profile']).first()
            active_profile = selected_profile
            status.changeActiveProfile(active_profile)
            isOn = active_profile.ap.start()

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

    if request.method == 'POST':
        c = Execte("serial -u /disk/username /disk/name /disk/firmware /memory/version /tmp && reboot")
        c.do()

    context = {
        'current_app_version' : current_app_version,
        'available_app_version' : available_app_version,
        'can_update' : can_update
    }
    return render(request, 'update.html', context)
