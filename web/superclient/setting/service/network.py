import psutil

def get_interfaces():
    return get_eth_interfaces() + get_wlan_interfaces();

def get_eth_interfaces():
    addrs = psutil.net_if_addrs()
    return [addr for addr in addrs.keys() if addr.startswith('eth')]

def get_wlan_interfaces():
    addrs = psutil.net_if_addrs()
    return [addr for addr in addrs.keys() if addr.startswith('wl')]
