from background_task import background
from superclient.action.models import ServiceStatus
from superclient.vpn.models import Configuration
from background_task.models import CompletedTask
from django.db.models import Q
from datetime import datetime, timedelta


@background(schedule=5, remove_existing_tasks=True)
def service_checker():
    status = ServiceStatus.get()    

    if status.on:
        start_services(status)
    else:
        stop_services(status)

@background(schedule=300, remove_existing_tasks=True)
def quota():
    dt_now = datetime.now()
    dt = dt_now - timedelta(hours=1, minutes=0, seconds=0)
    CompletedTask.objects.filter(Q(run_at__lt=dt)).delete()

def start_services(status: ServiceStatus):
    print('starting services...')

    hoptspot_profile = status.active_profile
    if hoptspot_profile and not hoptspot_profile.access_point.is_running():
        print('starting hotspot...')
        hoptspot_profile.access_point.start()
    else:
        print('[NO-CHANGE] hotspot service already started...')

    #if vpn not running
        #start_vpn_service(status)
    #else: no change


def start_vpn_service(status: ServiceStatus):

    if not status.active_vpn:
        print('selecting best vpn configuration...')
        selected_vpn = Configuration.objects.order_by('-priority', 'failed', '-success').first()
        if selected_vpn:
            status.change_active_vpn(selected_vpn)
            print(f'selected vpn configuration {selected_vpn.name}-{type(selected_vpn).__name__}')
        else:
            print(f'no qualify vpn configuration found.')
    else:
        print(f'[NO-CHANGE] use active vpn: {status.active_vpn.name}-{type(status.active_vpn).__name__}')

    #try to connect vpn use status.active_vpn


def stop_services(status: ServiceStatus):
    print('stoping services...')

    hoptspot_profile = status.active_profile
    if hoptspot_profile and hoptspot_profile.access_point.is_running():
        print('stoping hotspot...')
        hoptspot_profile.access_point.stop()
    else:
        print('[NO-CHANGE] hotspot service already stopped...')

    # if vpn running
        #