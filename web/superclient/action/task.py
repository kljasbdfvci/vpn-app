from superclient.action.models import ServiceStatus
from superclient.vpn.models import Configuration
from superclient.action.service.Router import Router
from superclient.setting.models import General
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
        if status.active_vpn == None:
            start_vpn_service(status)
        elif status.active_vpn != None and not Router(status.active_vpn).is_running():
            stop_vpn_service(status)
        elif status.selected_vpn != None and status.selected_vpn != status.active_vpn:
            stop_vpn_service(status)
        elif status.active_vpn not in list(Configuration.objects.filter(enable=True).all()):
            stop_vpn_service(status)
        elif status.apply:
            stop_vpn_service(status)
            status.toggle_apply()
        else:
            logging.info('[NO-CHANGE] vpn service already started.')
    else:
        if status.active_vpn != None:
            stop_vpn_service(status)
        elif status.apply:
            status.toggle_apply()
        else:
            logging.info('[NO-CHANGE] vpn service already stoped.')
        
    

def start_vpn_service(status: ServiceStatus):
    logging.info('starting vpn...')

    general = General.objects.first()
    vpn_list = []
    if status.selected_vpn == None:
        if general.vpn_smart_mode == general.VpnSmartMode.success_chance:
            logging.info('will use auto select vpn strategy in success chance mode.')
            vpn_list = list(Configuration.objects.filter(enable=True).all())
            vpn_list.sort(reverse=True, key=success_chance)
        elif general.vpn_smart_mode == general.VpnSmartMode.priority:
            logging.info('will use auto select vpn strategy in priority mode...')
            vpn_list = list(Configuration.objects.filter(enable=True).order_by('-priority').all())
        elif general.vpn_smart_mode == general.VpnSmartMode.circular:
            logging.info('will use auto select vpn strategy in circular mode.')
            vpn_list = list(Configuration.objects.filter(enable=True).order_by('id').all())
        
        if status.previous_active_vpn != None:
            index = vpn_list.index(status.previous_active_vpn)
            vpn_list = vpn_list[index + 1:] + vpn_list[:index] + vpn_list[index:index + 1]
    else:
        logging.info('will use static vpn strategy...')
        vpn_list.append(status.selected_vpn)

    i = 0
    vpn_str = "vpn list ["
    for vpn in vpn_list:
        vpn_str = vpn_str + "({}) {} ".format(i, vpn.title) 
        i = i + 1
    vpn_str = vpn_str + "]"
    logging.info(vpn_str)

    if(len(vpn_list) == 0):
        logging.error('vpn not found.')
    else:
        for vpn in vpn_list:
            logging.info("try connect to vpn configuration {}.".format(vpn.title))
            router = Router(vpn)
            res, output = router.ConnectVPN(timeout_arg=30, try_count_arg=6)
            vpn.add_log(output)
            if res == 0:
                vpn.increase_success()
                status.change_active_vpn(vpn)
                logging.info('vpn connected.')
                break
            else:
                vpn.increase_failed()
                status.change_active_vpn(None)
                logging.error('vpn connected failed.')
                continue
    return

def stop_vpn_service(status: ServiceStatus):
    logging.info('stoping vpn...')
    if status.active_vpn != None:
        logging.info("try disconnect vpn configuration {}.".format(status.active_vpn.title))
        router = Router(status.active_vpn)
        res, output = router.DisconnectVPN()
        status.change_active_vpn(None)
        if res == 0:
            logging.info('vpn disconnected.')
        else:
            logging.error('vpn disconnected failed.')

def success_chance(key):
    return key.success_chance
