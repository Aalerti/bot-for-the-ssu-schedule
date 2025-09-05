import asyncio
import logging
from aiogram import Bot, Dispatcher
# from config import load_config
from handlers import start, common_handlers
from parser.parse import parseSSU


logging.basicConfig(level=logging.INFO)


# config = load_config()


bot = Bot(token='7963082604:AAH8FgzclJ98-FR-rOyOXkQWPcufGmO48hQ')
dp = Dispatcher()


dp.include_router(start.router)
dp.include_router(common_handlers.router)


async def main():
    logging.info("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())