import asyncio
import sys
from contextlib import suppress

PING_WIN32 = ("ping", "-n", "3", "-w", "1000")
PING_POSIX = ("ping", "-b", "-n", "-q", "-c", "3", "-W1")
PING_TIMEOUT = 10


async def async_ping_ip_address(ip_address):
    """Ping an address to generate the arp cache."""
    ping_cmd = PING_WIN32 if sys.platform == "win32" else PING_POSIX
    pinger = await asyncio.create_subprocess_exec(
        *ping_cmd,
        ip_address,
        stdin=None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        await asyncio.wait_for(pinger.communicate(), PING_TIMEOUT)
    except asyncio.TimeoutError:
        if pinger:
            with suppress(TypeError):
                await pinger.kill()
            del pinger
        return False
    except AttributeError:
        return False
