import socket
import ifaddr
from ipaddress import ip_network


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


def get_network_and_broadcast_ip(local_ip, adapters):
    """Search adapters for the network and broadcast ip."""
    network_prefix = get_ip_prefix_from_adapters(local_ip, adapters)
    if network_prefix is None:
        return None
    network = ip_network(f"{local_ip}/{network_prefix}", False)
    return str(network.network_address), str(network.broadcast_address)


def get_ip_prefix_from_adapters(local_ip, adapters):
    """Find the nework prefix for an adapter."""
    for adapter in adapters:
        for ip in adapter.ips:
            if local_ip == ip.ip:
                return ip.network_prefix


def get_attrs_key(data, key):
    """Lookup an attrs key in pyroute2 data."""
    for attr_key, attr_value in data["attrs"]:
        if attr_key == key:
            return attr_value


def get_router_ip(ipr):
    """Obtain the router ip from the default route."""
    return get_attrs_key(ipr.get_default_routes()[0], "RTA_GATEWAY")


class SystemNetworkData:
    """Gather system network data."""

    def __init__(self, ip_route):
        """Init system network data."""
        self.ip_route = ip_route
        self.local_ip = None
        self.broadcast_ip = None
        self.router_ip = None
        self.nameservers = None

    def setup(self):
        """Obtain the local network data."""
        self.nameservers = load_resolv_conf()
        self.adapters = ifaddr.get_adapters()
        self.local_ip = get_local_ip()
        network_ip, self.broadcast_ip = get_network_and_broadcast_ip(
            self.local_ip, self.adapters
        )
        if self.ip_route:
            try:
                self.router_ip = get_router_ip(self.ip_route)
            except Exception:
                pass
        if not self.router_ip:
            # If we do not have working pyroute2, assume the router is .1
            self.router_ip = f"{network_ip[:-1]}1"
