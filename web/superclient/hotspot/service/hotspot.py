import psutil


def get_network_interfaces():
    addrs = psutil.net_if_addrs()
    return [addr for addr in addrs.keys() if addr.startswith('wl')]
