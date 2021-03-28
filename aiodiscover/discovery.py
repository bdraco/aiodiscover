import asyncio
from contextlib import suppress

from async_dns import DNSMessage, types
from async_dns.resolver import ProxyResolver
from pyroute2 import IPRoute

from .network import SystemNetworkData
from .utils import CONCURRENCY_LIMIT, gather_with_concurrency

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
        hostnames = await self._async_get_hostnames(sys_network_data)
        neighbours = await sys_network_data.async_get_neighbors(hostnames.values())
        return [
            {
                HOSTNAME: hostname,
                MAC_ADDRESS: neighbours[ip],
                IP_ADDRESS: ip,
            }
            for ip, hostname in hostnames.items()
            if ip in neighbours
        ]

    async def _async_get_hostnames(self, sys_network_data):
        """Lookup PTR records for all addresses in the network."""
        all_nameservers = list(sys_network_data.nameservers)
        router_ip = sys_network_data.router_ip
        if router_ip not in all_nameservers:
            all_nameservers.insert(0, router_ip)

        hostnames = {}
        for nameserver in all_nameservers:
            resolver = ProxyResolver(proxies=[nameserver])
            ips = [str(ip) for ip in sys_network_data.network.hosts()]
            tasks = [resolver.query(ip_to_ptr(str(ip)), types.PTR) for ip in ips]
            results = await gather_with_concurrency(
                CONCURRENCY_LIMIT, *tasks, return_exceptions=True
            )
            for idx, ip in enumerate(ips):
                if not isinstance(results[idx], DNSMessage):
                    continue
                record = results[idx].get_record((types.PTR,))
                if record is None:
                    continue
                hostnames[ip] = short_hostname(record)
        return hostnames
