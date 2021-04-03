import asyncio
import logging
from contextlib import suppress

from async_dns.core import REQUEST, DNSMessage, RandId, Record, types
from pyroute2 import IPRoute

from .network import SystemNetworkData

HOSTNAME = "hostname"
MAC_ADDRESS = "macaddress"
IP_ADDRESS = "ip"
MAX_ADDRESSES = 2048

DNS_RESPONSE_TIMEOUT = 2
MAX_DNS_TIMEOUT_DECLARE_DEAD_NAMESERVER = 5
DNS_PORT = 53

_LOGGER = logging.getLogger(__name__)


def ip_to_ptr(ip_address):
    """Convert an ip string to a PTR."""
    ipl = ip_address.split(".")
    ipl.reverse()
    return f"{'.'.join(ipl)}.in-addr.arpa"


def short_hostname(hostname):
    """The first part of the hostname."""
    return hostname.split(".")[0]


def dns_message_short_hostname(dns_message):
    """Get the short hostname from a dns message."""
    if not isinstance(dns_message, DNSMessage):
        return None
    record = dns_message.get_record((types.PTR,))
    if record is None:
        return None
    return short_hostname(record)


class PTRResolver:
    """Implement DNS PTR resolver."""

    def __init__(self, destination):
        """Init protocol for a destination."""
        self.destination = destination
        self.responses = {}
        self.send_qid = None
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
        msg = DNSMessage.parse(data)
        self.responses[msg.qid] = msg
        if msg.qid == self.send_qid:
            self.responded.set()

    def error_received(self, exc):
        """Error received."""
        self.error = exc
        self.responded.set()

    async def send_query(self, query):
        """Send a query and wait for a response."""
        self.responded.clear()
        self.send_qid = query.qid
        self.transport.sendto(query.pack(), self.destination)
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


def async_generate_ptr_query(rand_id, ip):
    """Generate a ptr query with the next random id."""
    req = DNSMessage(qr=REQUEST)
    req.qd = [Record(REQUEST, ip_to_ptr(str(ip)), types.PTR)]
    req.qid = rand_id.get()
    rand_id.put(req.qid)
    return req


async def async_query_for_ptr_with_proto(protocol, ips_to_lookup):
    """Send and receiver the PTR queries."""
    time_outs = 0
    query_for_ip = {}
    rand_id = RandId()
    for ip in ips_to_lookup:
        req = async_generate_ptr_query(rand_id, ip)
        query_for_ip[ip] = req.qid
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
            self.ip_route = IPRoute()

    async def async_discover(self):
        """Discover hosts on the network by ARP and PTR lookup."""
        sys_network_data = SystemNetworkData(self.ip_route)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sys_network_data.setup)
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
        ips = []
        for host in sys_network_data.network.hosts():
            if len(ips) > MAX_ADDRESSES:
                _LOGGER.debug(
                    "Max addresses of %s reached for network: %s",
                    MAX_ADDRESSES,
                    sys_network_data.network,
                )
                break
            ips.append(str(host))

        hostnames = {}
        for nameserver in all_nameservers:
            ips_to_lookup = [ip for ip in ips if ip not in hostnames]
            results = await async_query_for_ptrs(nameserver, ips_to_lookup)
            for idx, ip in enumerate(ips_to_lookup):
                short_host = dns_message_short_hostname(results[idx])
                if short_host is None:
                    continue
                hostnames[ip] = short_host
            if hostnames:
                # As soon as we have a responsive nameserver, there
                # is no need to query additional fallbacks
                break
        return hostnames
