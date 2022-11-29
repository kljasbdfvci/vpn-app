from superclient.action.models import ServiceStatus
from superclient.vpn.models import Configuration
from superclient.action.service.Router import Router
import time
from threading import Thread
import logging



def start():
    logging.info('start tasks...')
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
                logging.error(e)

            time.sleep(self.repeat_delay)


def service_checker():
    status = ServiceStatus.get()    

    if status.on:
        start_services(status)
    else:
        stop_services(status)


def start_services(status: ServiceStatus):
    logging.info('starting services...')

    if not get_active_router() or not get_active_router().is_running():
        logging.info('starting vpn...')
        start_vpn_service(status)
    else: logging.info('[NO-CHANGE] vpn service already started...')


def start_vpn_service(status: ServiceStatus):
    vpns = Configuration.objects.filter(enable=True).count()

    if status.selected_vpn:
        status.change_active_vpn(status.selected_vpn)
        vpns = 1
    else:
        logging.info('will use auto select vpn strategy...')

    for itr in range(vpns):
        if not status.active_vpn:
            logging.info('selecting best vpn configuration...')
            auto_selected_vpn = Configuration.objects.filter(enable=True).order_by('failed', '-priority', '-success').first()
            if auto_selected_vpn:
                status.change_active_vpn(auto_selected_vpn)
                logging.info(f'selected vpn configuration {auto_selected_vpn.title}')
            else:
                logging.info(f'no qualify vpn configuration found.')
                break
        else:
            logging.info(f'[NO-CHANGE] use active vpn: {status.active_vpn.title}')

        res, output = get_active_router().ConnectVPN(timeout_arg=30, try_count_arg=6)
        status.active_vpn.add_log(output)
        if res == 0:
            status.active_vpn.increase_success()
            logging.info(f'vpn connected.')
            break
        else:
            get_active_router().DisconnectVPN()
            status.change_active_vpn(None)
            status.active_vpn.increase_failed()
            logging.info(f'vpn not connect.')
            continue


def stop_services(status: ServiceStatus):
    logging.info('stoping services...')

    router = get_active_router()
    if router and router.is_running():
        logging.info('stoping vpn...')
        router.DisconnectVPN()
    else:
        logging.info('[NO-CHANGE] vpn service already stopped...')


def get_active_router():
    status = ServiceStatus.get()
    return Router(status.active_vpn) if status.active_vpn else None 

