#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from ipaddress import IPv4Address, IPv4Network, ip_address
from unittest.mock import MagicMock, patch

import pytest
from dns import message, rdatatype
from dns.message import Message

from aiodiscover import discovery

UDP_PTR_RESOLUTION_OCTETS = (
    b"\x8cV\x85\x80\x00\x01\x00\x01\x00\x00\x00\x00\x0249\x03107\x03168\x03192\x07"
    b"in-addr\x04arpa\x00\x00\x0c\x00\x01\xc0\x0c\x00\x0c\x00\x01\x00\x00\x00\x00"
    b"\x00(\x1bBroadlink_RMPROSUB-cc-ce-9f\x06koston\x03org\x00"
)

UDP_PTR_RESOLUTION_OCTETS_IDNA = (
    b"E\xca\x85\x80\x00\x01\x00\x01\x00\x00\x00\x00\x03237\x03209\x03168\x03192"
    b"\x07in-addr\x04arpa\x00\x00\x0c\x00\x01\xc0\x0c\x00\x0c\x00\x01"
    b"\x00\x00\x00\x00\x00\x1c\x0fAlxGarageSwitch\x06koston\x03org\x00"
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
            "4.5.5.6": "ff:bb:cc:0d:ee:ff",
        },
    ), patch(
        "aiodiscover.network.get_network",
        return_value=IPv4Network("1.2.3.0/24", False),
    ):
        hosts = await discover_hosts.async_discover()

    assert hosts == [
        {"hostname": "router", "ip": "1.2.3.4", "macaddress": "aa:bb:cc:dd:ee:ff"},
        {"hostname": "any", "ip": "4.5.5.6", "macaddress": "ff:bb:cc:0d:ee:ff"},
    ]

