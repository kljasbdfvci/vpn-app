from background_task import background
from superclient.action.models import ServiceStatus



@background(schedule=5, remove_existing_tasks=True)
def service_checker():
    status = ServiceStatus.get()    
    active_hotspot_profile = status.active_profile

    #TODO
    # if status.on 
        #if active_hotspot is not empty and hotspot is not running
            #run hotspot use status.active_profile
        #if vpn not running
            #if status.active_vpn is none
                #select a good vpn config and set status.active_vpn
            #run vpn with active_vpn if failed change status.active_vpn and try again
    # else: stop vpn and hotspot

    if active_hotspot_profile:
        print(f'active hotspot profile: {active_hotspot_profile.name}')
    else:
        print('no active hotspot profile')
