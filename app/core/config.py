import logging
from pathlib import Path

from pydantic_settings import BaseSettings
from pyowm.utils.config import get_default_config


logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
LOG_FILE_PATH = f'{BASE_DIR}/logs/bot.log'

class Settings(BaseSettings):
    BOT_TOKEN: str
    OWM_API_KEY: str
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = BASE_DIR.parent / ".env"


settings = Settings()


def get_owm_config():
    """Предоставляет доступ к конфигурации pyowm с измененённым на русский языком."""
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    return config_dict
