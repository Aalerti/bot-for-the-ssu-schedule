import asyncio
import logging
from aiogram import Bot, Dispatcher
# from config import load_config
from handlers import start, common_handlers


logging.basicConfig(level=logging.INFO)


# config = load_config()


# bot = Bot(token=config.token)
bot = Bot(token='7097280387:AAFfZN1Kt77d8tSaAbrtLR0wLcNji5WvT7k')
dp = Dispatcher()


dp.include_router(start.router)
dp.include_router(common_handlers.router)


async def main():
    logging.info("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())