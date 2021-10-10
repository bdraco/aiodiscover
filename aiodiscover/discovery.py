import asyncio
import logging
from contextlib import suppress

from dns import exception, message, rdatatype

from .network import SystemNetworkData

HOSTNAME = "hostname"
MAC_ADDRESS = "macaddress"
IP_ADDRESS = "ip"
MAX_ADDRESSES = 2048

DNS_RESPONSE_TIMEOUT = 2
MAX_DNS_TIMEOUT_DECLARE_DEAD_NAMESERVER = 5
DNS_PORT = 53

_LOGGER = logging.getLogger(__name__)


def short_hostname(hostname):
    """The first part of the hostname."""
    return hostname.split(".")[0]


def dns_message_short_hostname(dns_message):
    """Get the short hostname from a dns message."""
    if not isinstance(dns_message, message.Message) or not dns_message.answer:
        return None
    for answer in dns_message.answer:
        if answer.rdtype != rdatatype.PTR:
            continue
        for item in answer.items:
            return short_hostname(item.target.to_text())
    return None


class PTRResolver:
    """Implement DNS PTR resolver."""

    def __init__(self, destination):
        """Init protocol for a destination."""
        self.destination = destination
        self.responses = {}
        self.send_id = None
        self.responded = asyncio.Event()
        self.error = None

    def connection_lost(self, transport):
        """Connection lost."""

    def connection_made(self, transport):
        """Connection made."""
        self.transport = transport

    def datagram_received(self, data, addr):
        """Response recieved."""
        if addr != self.destination:
            return
        try:
            msg = message.from_wire(data)
        except exception.DNSException:
            return
        self.responses[msg.id] = msg
        if msg.id == self.send_id:
            self.responded.set()

    def error_received(self, exc):
        """Error received."""
        self.error = exc
        self.responded.set()

    async def send_query(self, query):
        """Send a query and wait for a response."""
        self.responded.clear()
        self.send_id = query.id
        self.transport.sendto(query.to_wire(), self.destination)
        await self.responded.wait()
        if self.error:
            raise self.error


async def async_query_for_ptrs(nameserver, ips_to_lookup):
    """Fetch PTR records for a list of ips."""
    destination = (nameserver, DNS_PORT)
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: PTRResolver(destination), remote_addr=destination
    )
    try:
        return await async_query_for_ptr_with_proto(protocol, ips_to_lookup)
    finally:
        transport.close()


def async_generate_ptr_query(ip):
    """Generate a ptr query with the next random id."""
    return message.make_query(ip.reverse_pointer, rdatatype.PTR)


async def async_query_for_ptr_with_proto(protocol, ips_to_lookup):
    """Send and receiver the PTR queries."""
    time_outs = 0
    query_for_ip = {}
    for ip in ips_to_lookup:
        req = async_generate_ptr_query(ip)
        query_for_ip[ip] = req.id
        try:
            await asyncio.wait_for(
                protocol.send_query(req), timeout=DNS_RESPONSE_TIMEOUT
            )
        except asyncio.TimeoutError:
            time_outs += 1
            if time_outs == MAX_DNS_TIMEOUT_DECLARE_DEAD_NAMESERVER:
                break
        except OSError:
            break

    return [protocol.responses.get(query_for_ip.get(ip)) for ip in ips_to_lookup]


class DiscoverHosts:
    """Discover hosts on the network by ARP and PTR lookup."""

    def __init__(self):
        """Init the discovery hosts."""
        self.ip_route = None
        with suppress(Exception):
            from pyroute2 import IPRoute  # pylint: disable=import-outside-toplevel

            self.ip_route = IPRoute()

    async def async_discover(self):
        """Discover hosts on the network by ARP and PTR lookup."""
        sys_network_data = SystemNetworkData(self.ip_route)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sys_network_data.setup)
        network = sys_network_data.network
        if network.num_addresses > MAX_ADDRESSES:
            _LOGGER.debug(
                "The network %s exceeds the maximum number of addresses, %s; No scanning performed",
                network,
                MAX_ADDRESSES,
            )
            return []
        hostnames = await self.async_get_hostnames(sys_network_data)
        neighbours = await sys_network_data.async_get_neighbors(hostnames.keys())
        return [
            {
                HOSTNAME: hostname,
                MAC_ADDRESS: neighbours[ip],
                IP_ADDRESS: ip,
            }
            for ip, hostname in hostnames.items()
            if ip in neighbours
        ]

    async def _async_get_nameservers(self, sys_network_data):
        """Get nameservers to query."""
        all_nameservers = list(sys_network_data.nameservers)
        router_ip = sys_network_data.router_ip
        if router_ip not in all_nameservers:
            neighbours = await sys_network_data.async_get_neighbors([router_ip])
            if router_ip in neighbours:
                all_nameservers.insert(0, router_ip)
        return all_nameservers

    async def async_get_hostnames(self, sys_network_data):
        """Lookup PTR records for all addresses in the network."""
        all_nameservers = await self._async_get_nameservers(sys_network_data)
        ips = list(sys_network_data.network.hosts())
        hostnames = {}
        for nameserver in all_nameservers:
            ips_to_lookup = [ip for ip in ips if str(ip) not in hostnames]
            results = await async_query_for_ptrs(nameserver, ips_to_lookup)
            for idx, ip in enumerate(ips_to_lookup):
                short_host = dns_message_short_hostname(results[idx])
                if short_host is None:
                    continue
                hostnames[str(ip)] = short_host
            if hostnames:
                # As soon as we have a responsive nameserver, there
                # is no need to query additional fallbacks
                break
        return hostnames
