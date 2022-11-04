from background_task import background
from superclient.action.models import ServiceStatus
from superclient.vpn.models import Configuration
from background_task.models import CompletedTask
from django.db.models import Q
from datetime import datetime, timedelta
from superclient.action.service.Router import Router



@background(schedule=300, remove_existing_tasks=True)
def quota():
    dt_now = datetime.now()
    dt = dt_now - timedelta(hours=1, minutes=0, seconds=0)
    CompletedTask.objects.filter(Q(run_at__lt=dt)).delete()


@background(schedule=0, remove_existing_tasks=True)
def service_checker():
    status = ServiceStatus.get()    

    if status.on:
        start_services(status)
    else:
        stop_services(status)


def start_services(status: ServiceStatus):
    print('starting services...')

    hoptspot_profile = status.active_profile
    if hoptspot_profile and not hoptspot_profile.access_point.is_running():
        print('starting hotspot...')
        hoptspot_profile.access_point.start()
    else:
        print('[NO-CHANGE] hotspot service already started...')


    if not get_active_router().is_running():
        print('starting vpn...')
        start_vpn_service(status)
    else: print('[NO-CHANGE] vpn service already started...')


def start_vpn_service(status: ServiceStatus):

    if not status.active_vpn:
        print('selecting best vpn configuration...')
        selected_vpn = Configuration.objects.filer(enable=True).order_by('failed', '-priority', '-success').first()
        if selected_vpn:
            status.change_active_vpn(selected_vpn)
            print(f'selected vpn configuration {selected_vpn.name}-{type(selected_vpn).__name__}')
        else:
            print(f'no qualify vpn configuration found.')
    else:
        print(f'[NO-CHANGE] use active vpn: {status.active_vpn.name}-{type(status.active_vpn).__name__}')

    get_active_router().ConnectVPN(timeout=30, try_count=6)


def stop_services(status: ServiceStatus):
    print('stoping services...')

    hoptspot_profile = status.active_profile
    if hoptspot_profile and hoptspot_profile.access_point.is_running():
        print('stoping hotspot...')
        hoptspot_profile.access_point.stop()
    else:
        print('[NO-CHANGE] hotspot service already stopped...')

    router = get_active_router()
    if router and router.is_running():
        print('stoping vpn...')
        router.DisconnectVPN()
    else:
        print('[NO-CHANGE] vpn service already stopped...')


def get_active_router():
    status = ServiceStatus.get()
    return Router(status.active_vpn, status.active_profile) if status.active_vpn and status.active_profile else None 

