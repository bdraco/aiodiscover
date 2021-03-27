#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiodiscover import DiscoverHosts


async def test_async_discover_hosts():
    """Verify discover hosts does not throw."""
    discover_hosts = DiscoverHosts()
    hosts = await discover_hosts.async_discover()
    assert isinstance(hosts, list)
