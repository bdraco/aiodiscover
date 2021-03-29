import asyncio
import cProfile
import pprint
import time

from pyprof2calltree import convert

from aiodiscover import DiscoverHosts

start_time = int(time.time() * 1000000)
pr = cProfile.Profile()
pr.enable()

discover_hosts = DiscoverHosts()
hosts = asyncio.run(discover_hosts.async_discover())
pprint.pprint(hosts)

pr.disable()
pr.create_stats()
pr.dump_stats(f"aiodiscover.{start_time}.cprof")
convert(pr.getstats(), f"callgrind.out.{start_time}")
