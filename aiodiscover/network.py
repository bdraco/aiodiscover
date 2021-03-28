import asyncio
import socket
from contextlib import suppress
from ipaddress import ip_address, ip_network

import ifaddr

ARP_TIMEOUT = 10
IGNORE_NETWORKS = (
    ip_network("169.254.0.0/16"),
    ip_network("127.0.0.0/8"),
    ip_network("::1/128"),
    ip_network("::ffff:127.0.0.0/104"),
    ip_network("224.0.0.0/4"),
)

IGNORE_MACS = ("00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff")


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


def _fill_neighbor(neighbours, ip, mac):
    """Add a neighbor if it is valid."""
    try:
        ip_addr = ip_address(ip)
    except ValueError:
        return
    if any(ip_addr in network for network in IGNORE_NETWORKS):
        return
    if mac in IGNORE_MACS:
        return
    neighbours[ip] = mac


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

    async def async_get_neighbors(self):
        """Get neighbors with best available method."""
        if self.ip_route:
            return await self._async_get_neighbors_ip_route()
        return await self._async_get_neighbors_arp()

    async def _async_get_neighbors_arp(self):
        """Get neighbors with arp command."""
        neighbours = {}
        arp = await asyncio.create_subprocess_exec(
            "arp",
            "-a" "-n",
            stdin=None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            out_data, _ = await asyncio.wait_for(arp.communicate(), ARP_TIMEOUT)
        except asyncio.TimeoutError:
            if arp:
                with suppress(TypeError):
                    await arp.kill()
                del arp
            return neighbours
        except AttributeError:
            return neighbours

        for line in out_data.splitlines():
            data = line.strip().split()
            if len(data) >= 4:
                _fill_neighbor(neighbours, data[1].strip("()"), data[3])

        return neighbours

    async def _async_get_neighbors_ip_route(self):
        """Get neighbors with pyroute2."""
        neighbours = {}
        for neighbour in self.ip_route.get_neighbours():
            ip = None
            mac = None
            for key, value in neighbour["attrs"]:
                if key == "NDA_DST":
                    ip = value
                elif key == "NDA_LLADDR":
                    mac = value
            if ip and mac:
                _fill_neighbor(neighbours, ip, mac)

        return neighbours
