import asyncio
import pprint

from aiodiscover import DiscoverHosts

discover_hosts = DiscoverHosts()
hosts = asyncio.run(discover_hosts.async_discover())
pprint.pprint(hosts)
