import asyncio
import logging
import sys
from contextlib import suppress

PING_WIN32 = ("ping", "-n", "3", "-w", "1000")
PING_POSIX = ("ping", "-b", "-n", "-q", "-c", "3", "-W1")
PING_MAC = ("ping", "-n", "-q", "-c", "3", "-W1")

PING_TIMEOUT = 10

_LOGGER = logging.getLogger(__name__)


async def async_ping_ip_address(ip_address):
    """Ping an address to generate the arp cache."""
    if sys.platform == "darwin":
        ping_cmd = PING_MAC
    elif sys.platform == "win32":
        ping_cmd = PING_WIN32
    else:
        ping_cmd = PING_POSIX
    pinger = await asyncio.create_subprocess_exec(
        *ping_cmd,
        ip_address,
        stdin=None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        out_data, err_data = await asyncio.wait_for(pinger.communicate(), PING_TIMEOUT)
        _LOGGER.debug("Ping output: %s (%s)", out_data, err_data)
    except asyncio.TimeoutError:
        if pinger:
            with suppress(TypeError):
                await pinger.kill()
            del pinger
        return False
    except AttributeError:
        return False
    except Exception:
        return False
    else:
        return True
