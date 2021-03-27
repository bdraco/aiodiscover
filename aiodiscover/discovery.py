import asyncio
import sys
from contextlib import suppress
from ipaddress import ip_address, ip_network

from async_dns import DNSMessage, types
from async_dns.resolver import ProxyResolver
from pyroute2 import IPRoute

from .network import SystemNetworkData

HOSTNAME = "hostname"
MAC_ADDRESS = "macaddress"
IP_ADDRESS = "ip"

PING_WIN32 = ("ping", "-n", "3", "-w", "1000")
PING_POSIX = ("ping", "-b", "-n", "-q", "-c", "3", "-W1")
PING_TIMEOUT = 10

IGNORE_NETWORKS = (
    ip_network("169.254.0.0/16"),
    ip_network("127.0.0.0/8"),
    ip_network("::1/128"),
    ip_network("::ffff:127.0.0.0/104"),
    ip_network("224.0.0.0/4"),
)

IGNORE_MACS = ("00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff")


def ip_to_ptr(ip_address):
    """Convert an ip string to a PTR."""
    ipl = ip_address.split(".")
    ipl.reverse()
    return f"{'.'.join(ipl)}.in-addr.arpa"


async def async_ping_ip_address(ip_address):
    """Ping an address to generate the arp cache."""
    ping_cmd = PING_WIN32 if sys.platform == "win32" else PING_POSIX
    pinger = await asyncio.create_subprocess_exec(
        *ping_cmd,
        ip_address,
        stdin=None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        await asyncio.wait_for(pinger.communicate(), PING_TIMEOUT)
    except asyncio.TimeoutError:
        if pinger:
            with suppress(TypeError):
                await pinger.kill()
            del pinger
        return False
    except AttributeError:
        return False


def get_neighbour_ip_mac(ip_route):
    """Return all neighbors by ip, mac."""
    neighbours = {}
    for neighbour in ip_route.get_neighbours():
        ip = None
        mac = None
        for key, value in neighbour["attrs"]:
            if key == "NDA_DST":
                ip = value
            elif key == "NDA_LLADDR":
                mac = value
        if ip and mac:
            ip_addr = ip_address(ip)
            if any(ip_addr in network for network in IGNORE_NETWORKS):
                continue
            if mac in IGNORE_MACS:
                continue
            neighbours[ip] = mac
    return neighbours


def short_hostname(hostname):
    """The first part of the hostname."""
    return hostname.split(".")[0]


class DiscoverHosts:
    """Discover hosts on the network by ARP and PTR lookup."""

    def __init__(self):
        """Init the discovery hosts."""
        self.ip_route = IPRoute()

    async def async_discover(self):
        """Discover hosts on the network by ARP and PTR lookup."""
        sys_network_data = SystemNetworkData(self.ip_route)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sys_network_data.setup)

        all_nameservers = list(sys_network_data.nameservers)
        router_ip = sys_network_data.router_ip
        if router_ip:
            if router_ip not in all_nameservers:
                all_nameservers.insert(0, router_ip)

        resolver = ProxyResolver(proxies=all_nameservers)
        await async_ping_ip_address(sys_network_data.broadcast_ip)

        neighbours = await loop.run_in_executor(
            None, get_neighbour_ip_mac, self.ip_route
        )
        tasks = [resolver.query(ip_to_ptr(ip), types.PTR) for ip in neighbours]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        discovered = []
        for idx, ip in enumerate(neighbours):
            mac = neighbours[ip]
            if isinstance(results[idx], DNSMessage):
                record = results[idx].get_record((types.PTR,))
                if record is not None:
                    hostname = short_hostname(record)
                    discovered.append(
                        {HOSTNAME: hostname, MAC_ADDRESS: mac, IP_ADDRESS: ip}
                    )

        return discovered
