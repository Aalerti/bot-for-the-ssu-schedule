import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    if token is None:
        raise ValueError("Токен не найден! Проверь файл .env")
    return type('Config', (), {'token': token})()