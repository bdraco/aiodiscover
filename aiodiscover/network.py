import socket


def load_resolv_conf():
    """Load the resolv.conf."""
    with open("/etc/resolv.conf", "r") as file:
        lines = tuple(file)
    nameservers = set()
    for line in lines:
        line = line.strip()
        if not len(line):
            continue
        if line[0] in ("#", ";"):
            continue
        key, value = line.split(None, 1)
        if key == "nameserver":
            nameservers.add(value)
    return list(nameservers)


def get_local_ip():
    """Find the local ip address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


def get_addr_data(local_ip, ipr):
    for addr_data in ipr.get_addr():
        for key, value in addr_data["attrs"]:
            if key == "IFA_ADDRESS" and value == local_ip:
                return addr_data


def get_broadcast_ip(local_ip, ipr):
    addr_data = get_addr_data(local_ip, ipr)
    if addr_data is None:
        return None
    return get_attrs_key(addr_data, "IFA_BROADCAST")


def get_attrs_key(data, key):
    for attr_key, attr_value in data["attrs"]:
        if attr_key == key:
            return attr_value


def get_router_ip(ipr):
    return get_attrs_key(ipr.get_default_routes()[0], "RTA_GATEWAY")


class SystemNetworkData:
    def __init__(self, ip_route):
        self.ip_route = ip_route
        self.local_ip = None
        self.broadcast_ip = None
        self.router_ip = None
        self.nameservers = None

    def setup(self):
        self.local_ip = get_local_ip()
        self.broadcast_ip = get_broadcast_ip(self.local_ip, self.ip_route)
        self.nameservers = load_resolv_conf()
        try:
            self.router_ip = get_router_ip(self.ip_route)
        except Exception:
            pass
