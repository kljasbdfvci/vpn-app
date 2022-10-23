import psutil


def get_network_interfaces():
    addrs = psutil.net_if_addrs()
    return addrs.keys()