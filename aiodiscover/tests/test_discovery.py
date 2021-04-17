#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from unittest.mock import MagicMock, patch

import pytest

from aiodiscover import discovery

UDP_PTR_RESOLUTION_OCTETS = (
    b"\x8cV\x85\x80\x00\x01\x00\x01\x00\x00\x00\x00\x0249\x03107\x03168\x03192\x07"
    b"in-addr\x04arpa\x00\x00\x0c\x00\x01\xc0\x0c\x00\x0c\x00\x01\x00\x00\x00\x00"
    b"\x00(\x1bBroadlink_RMPROSUB-cc-ce-9f\x06koston\x03org\x00"
)


@pytest.mark.asyncio
async def test_async_discover_hosts():
    """Verify discover hosts does not throw."""
    discover_hosts = discovery.DiscoverHosts()
    with patch.object(discovery, "MAX_ADDRESSES", 16):
        hosts = await discover_hosts.async_discover()
    assert isinstance(hosts, list)


@pytest.mark.asyncio
async def test_async_discover_hosts_with_dns_mock():
    """Verify discover hosts does not throw."""
    discover_hosts = discovery.DiscoverHosts()
    with patch.object(discovery, "MAX_ADDRESSES", 2), patch(
        "aiodiscover.discovery.dns_message_short_hostname", return_value="router"
    ):
        hosts = await discover_hosts.async_discover()
    assert isinstance(hosts, list)


@pytest.mark.asyncio
async def test_async_discover_hosts_with_dns_mock_neighbor_mock():
    """Verify discover hosts does not throw."""
    discover_hosts = discovery.DiscoverHosts()

    async def _async_get_hostnames(sys_network_data):
        return {"1.2.3.4": "router", "4.5.5.6": "any"}

    discover_hosts.async_get_hostnames = _async_get_hostnames
    with patch(
        "aiodiscover.network.SystemNetworkData.async_get_neighbors",
        return_value={
            "1.2.3.4": "aa:bb:cc:dd:ee:ff",
            "4.5.5.6": "ff:bb:cc:dd:ee:ff",
        },
    ):
        hosts = await discover_hosts.async_discover()

    assert hosts == [
        {"hostname": "router", "ip": "1.2.3.4", "macaddress": "aa:bb:cc:dd:ee:ff"},
        {"hostname": "any", "ip": "4.5.5.6", "macaddress": "ff:bb:cc:dd:ee:ff"},
    ]


@pytest.mark.asyncio
async def test_ptr_resolver_protocol_ignores_other_sources():
    """Test that the PTRResolver ignores responses from unexpected sources."""
    destination = ("192.168.107.1", discovery.DNS_PORT)
    other_destination = ("192.168.107.2", discovery.DNS_PORT)
    ptr_resolver = discovery.PTRResolver(destination)
    ptr_resolver.datagram_received(UDP_PTR_RESOLUTION_OCTETS, destination)
    assert 35926 in ptr_resolver.responses
    ptr_resolver.responses = {}
    ptr_resolver.datagram_received(UDP_PTR_RESOLUTION_OCTETS, other_destination)
    assert 35926 not in ptr_resolver.responses


@pytest.mark.asyncio
async def test_ptr_resolver_can_parse():
    """Test that the PTRResolver can parse a response."""
    destination = ("192.168.107.1", discovery.DNS_PORT)
    ptr_resolver = discovery.PTRResolver(destination)
    ptr_resolver.datagram_received(UDP_PTR_RESOLUTION_OCTETS, destination)
    assert 35926 in ptr_resolver.responses
    assert (
        discovery.dns_message_short_hostname(ptr_resolver.responses[35926]).lower()
        == "broadlink_rmprosub-cc-ce-9f"
    )


@pytest.mark.asyncio
async def test_ptr_resolver_error_received():
    """Test that the PTRResolver raises exception from error_received."""
    destination = ("192.168.107.1", discovery.DNS_PORT)
    ptr_resolver = discovery.PTRResolver(destination)
    ptr_resolver.transport = MagicMock()
    loop = asyncio.get_running_loop()
    loop.call_later(0.01, ptr_resolver.error_received, ConnectionRefusedError)
    req = discovery.async_generate_ptr_query("1.2.3.4")
    with pytest.raises(ConnectionRefusedError):
        await ptr_resolver.send_query(req)


@pytest.mark.asyncio
async def test_async_query_for_ptr_with_proto():
    """Test async_query_for_ptr_with_proto handles OSErrors without raising."""
    destination = ("192.168.107.1", discovery.DNS_PORT)
    ptr_resolver = discovery.PTRResolver(destination)
    ptr_resolver.transport = MagicMock()
    loop = asyncio.get_running_loop()
    ptr_resolver.datagram_received(UDP_PTR_RESOLUTION_OCTETS, destination)
    loop.call_later(0.01, ptr_resolver.error_received, ConnectionRefusedError)
    await discovery.async_query_for_ptr_with_proto(ptr_resolver, ["1.2.3.4"])
    assert 35926 in ptr_resolver.responses
