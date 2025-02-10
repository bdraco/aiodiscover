import asyncio
import pprint

from aiodiscover import DiscoverHosts


async def run() -> None:
    pprint.pprint(DiscoverHosts().async_discover())


asyncio.run(run())
