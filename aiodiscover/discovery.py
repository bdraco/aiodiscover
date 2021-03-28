import asyncio
from contextlib import suppress

from async_dns import DNSMessage, types
from async_dns.resolver import ProxyResolver
from pyroute2 import IPRoute

from .network import SystemNetworkData
from .ping import async_ping_ip_address

HOSTNAME = "hostname"
MAC_ADDRESS = "macaddress"
IP_ADDRESS = "ip"


def ip_to_ptr(ip_address):
    """Convert an ip string to a PTR."""
    ipl = ip_address.split(".")
    ipl.reverse()
    return f"{'.'.join(ipl)}.in-addr.arpa"


def short_hostname(hostname):
    """The first part of the hostname."""
    return hostname.split(".")[0]


class DiscoverHosts:
    """Discover hosts on the network by ARP and PTR lookup."""

    def __init__(self):
        """Init the discovery hosts."""
        self.ip_route = None
        with suppress(Exception):
            self.ip_route = IPRoute()

    async def async_discover(self):
        """Discover hosts on the network by ARP and PTR lookup."""
        sys_network_data = SystemNetworkData(self.ip_route)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sys_network_data.setup)

        all_nameservers = list(sys_network_data.nameservers)
        router_ip = sys_network_data.router_ip
        if router_ip not in all_nameservers:
            all_nameservers.insert(0, router_ip)

        await async_ping_ip_address(sys_network_data.broadcast_ip)

        neighbours = await sys_network_data.async_get_neighbors()
        discovered = {}

        for nameserver in all_nameservers:
            resolver = ProxyResolver(proxies=[nameserver])
            tasks = [resolver.query(ip_to_ptr(ip), types.PTR) for ip in neighbours]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for idx, ip in enumerate(neighbours):
                mac = neighbours[ip]
                if not isinstance(results[idx], DNSMessage):
                    continue
                record = results[idx].get_record((types.PTR,))
                if record is None:
                    continue
                discovered[mac] = {
                    HOSTNAME: short_hostname(record),
                    MAC_ADDRESS: mac,
                    IP_ADDRESS: ip,
                }

        return list(discovered.values())
