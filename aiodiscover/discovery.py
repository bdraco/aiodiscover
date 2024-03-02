from __future__ import annotations

import asyncio
import logging
import random
from contextlib import suppress
from functools import lru_cache
from ipaddress import IPv4Address
from typing import TYPE_CHECKING, Any, Optional, cast

from dns import exception, message, rdatatype
from dns.message import Message, QueryMessage
from dns.name import Name

from .network import SystemNetworkData

if TYPE_CHECKING:
    from pyroute2.iproute import IPRoute  # noqa: F401

HOSTNAME = "hostname"
MAC_ADDRESS = "macaddress"
IP_ADDRESS = "ip"
MAX_ADDRESSES = 2048

DNS_RESPONSE_TIMEOUT = 2
MAX_DNS_TIMEOUT_DECLARE_DEAD_NAMESERVER = 5
DNS_PORT = 53

_LOGGER = logging.getLogger(__name__)


class FastName(Name):
    """A fast name."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init."""
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "_to_wire", super().to_wire())

    def to_wire(self, *args: Any, **kwargs: Any) -> bytes:
        """Convert to wire format."""
        if args or kwargs:
            return super().to_wire(*args, **kwargs)
        return self._to_wire


def short_hostname(hostname: str) -> str:
    """The first part of the hostname."""
    return hostname.split(".")[0]


def dns_message_short_hostname(dns_message: message.Message | None) -> str | None:
    """Get the short hostname from a dns message."""
    if not isinstance(dns_message, message.Message) or not dns_message.answer:
        return None
    for answer in dns_message.answer:
        if answer.rdtype != rdatatype.PTR:
            continue
        for item in answer.items:
            return short_hostname(item.target.to_unicode())
    return None


def set_exception_if_not_done(future: asyncio.Future, exc: Exception) -> None:
    """Set result if not done."""
    if not future.done():
        future.set_exception(exc)


class PTRResolver:
    """Implement DNS PTR resolver."""

    def __init__(self, destination: tuple[str, int]) -> None:
        """Init protocol for a destination."""
        self.destination: tuple[str, int] = destination
        self.responses: dict[int, Message] = {}
        self.send_id: int | None = None
        self.responded: Optional[asyncio.Future[None]] = None
        self.error: Exception | None = None
        self.loop = asyncio.get_running_loop()

    def connection_lost(self, ex: Exception | None) -> None:
        """Connection lost."""

    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        """Connection made."""
        self.transport = transport

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        """Response received."""
        if addr != self.destination:
            return
        try:
            msg = message.from_wire(data)
        except exception.DNSException:
            return
        self.responses[msg.id] = msg
        if msg.id == self.send_id and not self.responded.done():
            self.responded.set_result(None)

    def error_received(self, exc: Exception) -> None:
        """Error received."""
        if not self.responded.done():
            self.responded.set_exception(exc)

    async def send_query(self, query: Message, timeout: float) -> None:
        """Send a query and wait for a response."""
        loop = self.loop
        self.responded = loop.create_future()
        self.send_id = query.id
        self.transport.sendto(query.to_wire(), self.destination)
        handle = self.loop.call_at(
            loop.time() + timeout,
            set_exception_if_not_done,
            self.responded,
            asyncio.TimeoutError,
        )
        try:
            await self.responded
        finally:
            if not self.responded.cancelled() and not self.responded.exception():
                handle.cancel()


async def async_query_for_ptrs(
    nameserver: str, ips_to_lookup: list[IPv4Address]
) -> list[Message | None]:
    """Fetch PTR records for a list of ips."""
    destination = (nameserver, DNS_PORT)
    loop = asyncio.get_running_loop()

    transport_protocol = await loop.create_datagram_endpoint(
        lambda: PTRResolver(destination), remote_addr=destination  # type: ignore
    )
    transport = cast(asyncio.DatagramTransport, transport_protocol[0])
    protocol = cast(PTRResolver, transport_protocol[1])
    try:
        return await async_query_for_ptr_with_proto(protocol, ips_to_lookup)
    finally:
        transport.close()


def async_mutate_ptr_query(req: QueryMessage, ip: IPv4Address, id_: int) -> Message:
    """Mutate a ptr query with the next random id."""
    req.id = id_
    req.question[0].name = _get_name(ip.reverse_pointer)


@lru_cache(maxsize=MAX_ADDRESSES)
def _get_name(reverse_pointer: str) -> FastName:
    """Get the FastName for a reverse pointer."""
    return FastName(
        (label.encode("ascii") for label in (*reverse_pointer.split("."), ""))
    )


async def async_query_for_ptr_with_proto(
    protocol: PTRResolver, ips_to_lookup: list[IPv4Address]
) -> list[Message | None]:
    """Send and receiver the PTR queries."""
    time_outs = 0
    query_for_ip = {}
    used_ids = {0}
    req = message.make_query(ips_to_lookup[0].reverse_pointer, rdatatype.PTR)
    id_ = 0
    for ip in ips_to_lookup:
        while id_ in used_ids:
            id_ = random.randint(1, 65535)
        used_ids.add(id_)
        async_mutate_ptr_query(req, ip, id_)
        query_for_ip[ip] = id_
        try:
            await protocol.send_query(req, DNS_RESPONSE_TIMEOUT)
        except asyncio.TimeoutError:
            time_outs += 1
            if time_outs == MAX_DNS_TIMEOUT_DECLARE_DEAD_NAMESERVER:
                break
        except OSError:
            break

    return [protocol.responses.get(query_for_ip.get(ip)) for ip in ips_to_lookup]  # type: ignore


class DiscoverHosts:
    """Discover hosts on the network by ARP and PTR lookup."""

    def __init__(self) -> None:
        """Init the discovery hosts."""
        self._sys_network_data: SystemNetworkData | None = None

    def _setup_sys_network_data(self) -> None:
        ip_route: "IPRoute" | None = None
        with suppress(Exception):
            from pyroute2.iproute import (  # noqa: F811
                IPRoute,
            )  # type: ignore # pylint: disable=import-outside-toplevel

            ip_route = IPRoute()
        sys_network_data = SystemNetworkData(ip_route)
        sys_network_data.setup()
        self._sys_network_data = sys_network_data

    async def async_discover(self) -> list[dict[str, str]]:
        """Discover hosts on the network by ARP and PTR lookup."""
        if not self._sys_network_data:
            await asyncio.get_running_loop().run_in_executor(
                None, self._setup_sys_network_data
            )
        sys_network_data = self._sys_network_data
        network = sys_network_data.network
        assert network is not None
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

    async def _async_get_nameservers(
        self, sys_network_data: SystemNetworkData
    ) -> list[str]:
        """Get nameservers to query."""
        all_nameservers = list(sys_network_data.nameservers)
        router_ip = sys_network_data.router_ip
        assert router_ip is not None
        if router_ip not in all_nameservers:
            neighbours = await sys_network_data.async_get_neighbors([router_ip])
            if router_ip in neighbours:
                all_nameservers.insert(0, router_ip)
        return all_nameservers

    async def async_get_hostnames(
        self, sys_network_data: SystemNetworkData
    ) -> dict[str, str]:
        """Lookup PTR records for all addresses in the network."""
        all_nameservers = await self._async_get_nameservers(sys_network_data)
        assert sys_network_data.network is not None
        ips = list(sys_network_data.network.hosts())
        hostnames: dict[str, str] = {}
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
