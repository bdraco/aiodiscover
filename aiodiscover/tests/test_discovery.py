#!/usr/bin/env python
import asyncio
import sys
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Network
from typing import Any
from unittest.mock import patch

import pytest

from aiodiscover import discovery

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.mark.asyncio
async def test_async_discover_hosts() -> None:
    """Verify discover hosts does not throw."""
    discover_hosts = discovery.DiscoverHosts()
    with patch.object(discovery, "MAX_ADDRESSES", 16):
        hosts = await discover_hosts.async_discover()
    assert isinstance(hosts, list)


@pytest.mark.asyncio
async def test_async_discover_hosts_with_dns_mock() -> None:
    """Verify discover hosts does not throw."""
    discover_hosts = discovery.DiscoverHosts()
    with (
        patch.object(discovery, "MAX_ADDRESSES", 2),
        patch(
            "aiodiscover.discovery.dns_message_short_hostname", return_value="router"
        ),
    ):
        hosts = await discover_hosts.async_discover()
    assert isinstance(hosts, list)


@pytest.mark.asyncio
async def test_async_discover_hosts_with_dns_mock_neighbor_mock() -> None:
    """Verify discover hosts does not throw."""
    discover_hosts = discovery.DiscoverHosts()

    async def _async_get_hostnames(sys_network_data: Any) -> dict[str, str]:
        return {"1.2.3.4": "router", "4.5.5.6": "any"}

    discover_hosts.async_get_hostnames = _async_get_hostnames  # type: ignore
    with (
        patch(
            "aiodiscover.network.SystemNetworkData.async_get_neighbors",
            return_value={
                "1.2.3.4": "aa:bb:cc:dd:ee:ff",
                "4.5.5.6": "ff:bb:cc:0d:ee:ff",
            },
        ),
        patch(
            "aiodiscover.network.get_network",
            return_value=IPv4Network("1.2.3.0/24", False),
        ),
    ):
        hosts = await discover_hosts.async_discover()

    assert hosts == [
        {"hostname": "router", "ip": "1.2.3.4", "macaddress": "aa:bb:cc:dd:ee:ff"},
        {"hostname": "any", "ip": "4.5.5.6", "macaddress": "ff:bb:cc:0d:ee:ff"},
    ]


@pytest.mark.asyncio
async def test_async_query_for_ptrs() -> None:
    """Test async_query_for_ptrs handles missing ips."""
    loop = asyncio.get_running_loop()
    count = 0

    @dataclass
    class MockReply:
        name: str

    def mock_query(*args: Any, **kwargs: Any) -> Any:
        nonlocal count
        count += 1
        future = loop.create_future()
        if count == 2:
            future.set_exception(Exception("test"))
        else:
            future.set_result(MockReply(name=f"name{count}"))
        return future

    with (
        patch.object(discovery, "DNS_RESPONSE_TIMEOUT", 0),
        patch("aiodiscover.discovery.DNSResolver.query", mock_query),
    ):
        response = await discovery.async_query_for_ptrs(
            "192.168.107.1",
            [
                IPv4Address("192.168.107.2"),
                IPv4Address("192.168.107.3"),
                IPv4Address("192.168.107.4"),
            ],
        )

    assert len(response) == 3
    assert response[0].name == "name1"  # type: ignore
    assert response[1] is None  # type: ignore
    assert response[2].name == "name3"  # type: ignore


@pytest.mark.asyncio
async def test_async_query_for_ptrs_chunked() -> None:
    """Test async_query_for_ptrs chunkeds."""
    loop = asyncio.get_running_loop()
    count = 0

    @dataclass
    class MockReply:
        name: str

    def mock_query(*args: Any, **kwargs: Any) -> Any:
        nonlocal count
        count += 1
        future = loop.create_future()
        if count == 2:
            future.set_exception(Exception("test"))
        else:
            future.set_result(MockReply(name=f"name{count}"))
        return future

    with (
        patch.object(discovery, "DNS_RESPONSE_TIMEOUT", 0),
        patch("aiodiscover.discovery.DNSResolver.query", mock_query),
        patch.object(discovery, "QUERY_BUCKET_SIZE", 1),
    ):
        response = await discovery.async_query_for_ptrs(
            "192.168.107.1",
            [
                IPv4Address("192.168.107.2"),
                IPv4Address("192.168.107.3"),
                IPv4Address("192.168.107.4"),
            ],
        )

    assert len(response) == 3
    assert response[0].name == "name1"  # type: ignore
    assert response[1] is None
    assert response[2].name == "name3"  # type: ignore
