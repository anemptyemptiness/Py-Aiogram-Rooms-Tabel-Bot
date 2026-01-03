import asyncio
import logging

from aiogram.exceptions import TelegramNetworkError
from aiohttp import ServerDisconnectedError

logger = logging.getLogger(__name__)


async def safe_tg_call(coro, attempts=4):
    for i in range(attempts):
        try:
            return await coro()
        except (ServerDisconnectedError, TelegramNetworkError) as e:
            if "disconnected" in str(e).lower() and i < attempts - 1:
                wait = 2 ** i
                logger.warning(f"⚠ TG disconnect, retry {i+1}/{attempts} in {wait}s")

                await asyncio.sleep(wait)
            else:
                raise