import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# файл config_reader.py можно взять из репозитория
# пример — в первой главе
from config import config
from handlers import common, profile, acquaintance
from db import RandomCoffeeDB

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())
    await common.set_main_menu(bot)
    dp.include_router(common.router)
    dp.include_router(profile.router)
    dp.include_router(acquaintance.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
