import asyncio
import logging
import sys
from threading import Thread

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramNetworkError, TelegramAPIError
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import TCPConnector

from src.config import settings, redis
from src.menu_commands import set_default_commands
from src.handlers import (
    router_authorise,
    router_attractions,
    router_encashment,
    router_finish,
    router_start_shift,
    router_admin,
)
from src.autoposting.check_for_revenue import creating_new_loop_for_checking_revenue


async def main() -> None:
    session = AiohttpSession(timeout=settings.HTTP_TIMEOUT)

    bot = Bot(token=settings.TOKEN, session=session)
    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    logging.basicConfig(
        format='[{asctime}] #{levelname:8} {filename}: '
               '{lineno} - {name} - {message}',
        style="{",
        level=logging.WARNING,
        filename="logs.log",
        filemode="w",
    )

    # Подключаем роутеры к диспетчеру
    dp.include_router(router_authorise)
    dp.include_router(router_start_shift)
    dp.include_router(router_encashment)
    dp.include_router(router_attractions)
    dp.include_router(router_finish)
    dp.include_router(router_admin)

    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    global_loop = asyncio.get_event_loop()
    auto_checking_revenue_thread = Thread(target=creating_new_loop_for_checking_revenue, args=(global_loop, bot))
    auto_checking_revenue_thread.start()

    while True:
        try:
            print("Бот успешно запущен!")
            await dp.start_polling(bot)
        except (TelegramNetworkError, TelegramAPIError) as tne:
            await bot.send_message(settings.ADMIN_ID, f"Ошибка от Телеграм: {tne}. Reconnecting...")
            await asyncio.sleep(5)
        except Exception as e:
            await bot.send_message(settings.ADMIN_ID, f"Иная ошибка Exception: {e}. Reconnecting...")
            await asyncio.sleep(5)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as ki:
        print("Бот успешно остановлен!")
    except Exception as e:
        print(f"Ошибка: {e}")
