import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import load_config
from handlers import start, common_handlers

# Настраиваем логирование, чтобы видеть что происходит
logging.basicConfig(level=logging.INFO)

# Загружаем конфиг
config = load_config()

# Инициализируем бот и диспетчер
bot = Bot(token=config.token)
dp = Dispatcher()

# Регистрируем роутеры из обработчиков
dp.include_router(start.router)
dp.include_router(common_handlers.router)

# Главная функция
async def main():
    logging.info("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())