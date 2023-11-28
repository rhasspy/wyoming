#!/usr/bin/env python3
"""Runs mDNS zeroconf service for Home Assistant discovery."""
import logging
import socket
from typing import Optional

_LOGGER = logging.getLogger()

try:
    from zeroconf.asyncio import AsyncServiceInfo, AsyncZeroconf
except ImportError:
    _LOGGER.fatal("pip install zeroconf")
    raise

MDNS_TARGET_IP = "224.0.0.251"


async def register_server(name: str, port: int, host: Optional[str] = None) -> None:
    if not host:
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_sock.setblocking(False)
        test_sock.connect((MDNS_TARGET_IP, 1))
        host = test_sock.getsockname()[0]
        _LOGGER.debug("Detected IP: %s", host)

    assert host

    service_info = AsyncServiceInfo(
        "_wyoming._tcp.local.",
        f"{name}._wyoming._tcp.local.",
        addresses=[socket.inet_aton(host)],
        port=port,
    )
    aiozc = AsyncZeroconf()
    await aiozc.async_register_service(service_info)
