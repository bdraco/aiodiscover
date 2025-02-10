import asyncio
import logging
import pprint

from aiodiscover import DiscoverHosts

logging.basicConfig(level=logging.DEBUG)


async def run() -> None:
    pprint.pprint(await DiscoverHosts().async_discover())


asyncio.run(run())
