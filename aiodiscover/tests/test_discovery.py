#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from unittest.mock import patch
from aiodiscover import discovery


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
