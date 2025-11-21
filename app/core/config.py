import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from pyowm.utils.config import get_default_config


logger = logging.getLogger(__name__)

# Получаем значения конфигурации через переменные
load_dotenv()  # загрузит .env в окружение

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWM_API_KEY = os.getenv("OWM_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

BASE_DIR = Path(__file__).parent.parent # определяем базовый путь проекта
LOG_FILE_PATH = f'{BASE_DIR}/logs/bot.log' # расположение файла для логов


def get_owm_config():
    """Предоставляет доступ к конфигурации pyowm с измененённым на русский языком."""
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    return config_dict
