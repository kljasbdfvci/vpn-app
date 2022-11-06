from superclient.action.models import ServiceStatus
from superclient.vpn.models import Configuration
from superclient.action.service.Router import Router
import time
from threading import Thread


def start():
    print('start tasks...')
    TaskThread().start()


class TaskThread(Thread):

    start_delay = 5
    repeat_delay = 5

    def run(self):
        time.sleep(self.start_delay)

        while True:
            try:

                service_checker()

            except Exception as e:
                print(e)

            time.sleep(self.repeat_delay)


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
    elif status.active_profile != status.selected_profile:
        print('changing active hotspot profile...')
        status.change_active_profile(status.selected_profile)
        hoptspot_profile.access_point.stop()
        # will start on next iteration
    else:
        print('[NO-CHANGE] hotspot service already started...')

    if get_active_router() and not get_active_router().is_running():
        print('starting vpn...')
        start_vpn_service(status)
    elif status.active_vpn != status.selected_vpn:
        print('changing active vpn...')
        status.change_active_vpn(status.selected_vpn)
        router = get_active_router()
        router.DisconnectVPN()
        # will start on next iteration
    else: print('[NO-CHANGE] vpn service already started...')


def start_vpn_service(status: ServiceStatus):
    vpns = Configuration.objects.filter(enable=True).count()

    if status.selected_vpn:
        status.change_active_vpn(status.selected_vpn)
        vpns = 1
    else:
        print('will use auto select vpn strategy...')

    for itr in range(vpns):
        if not status.active_vpn:
            print('selecting best vpn configuration...')
            auto_selected_vpn = Configuration.objects.filer(enable=True).order_by('failed', '-priority', '-success').first()
            if auto_selected_vpn:
                status.change_active_vpn(auto_selected_vpn)
                print(f'selected vpn configuration {auto_selected_vpn.title}')
            else:
                print(f'no qualify vpn configuration found.')
                break
        else:
            print(f'[NO-CHANGE] use active vpn: {status.active_vpn.title}')

        res, output = get_active_router().ConnectVPN(timeout=30, try_count=6)
        status.active_vpn.add_log(output)
        if res == 0:
            status.active_vpn.increase_success()
            print(f'vpn connected.')
            break
        else:
            get_active_router().DisconnectVPN()
            status.change_active_vpn(None)
            status.active_vpn.increase_failed()
            print(f'vpn not connect.')



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

