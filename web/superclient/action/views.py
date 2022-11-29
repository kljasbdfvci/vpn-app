from django.shortcuts import render
from pathlib import Path
from superclient.vpn.models import Configuration
from superclient.action.service.Router import Router
from .models import ServiceStatus as Status
from .service.Execte import *
from .service.Network import *


def index(request):
    status = Status.get()

    if request.method == 'POST':
        if 'apply' in dict.keys():
            Network().Apply()
            if status.on:
                Router(status.active_vpn).DisconnectVPN()

        else:
            if not status.on:
                selected_vpn = Configuration.objects.filter(id=request.POST.dict()['vpn']).first()
                status.change_selected_vpn(selected_vpn)
        
            status.toggle_on()

    submitText = 'Off' if status.on else 'On'
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
        'vpns': vpns,
        'submitText': submitText, 
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
