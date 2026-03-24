import logging
import time

import telebot
from pyowm.owm import OWM

from core.config import settings

logger = logging.getLogger(__name__)

# Используем значения конфигурации, импортированные из config.py
BOT_TOKEN = settings.BOT_TOKEN
OWM_API_KEY = settings.OWM_API_KEY
LOG_LEVEL = settings.LOG_LEVEL
LOG_FILE_PATH = settings.LOG_FILE_PATH

# Настраиваем логирование
try:
    log_level = getattr(logging, settings.LOG_LEVEL)
except AttributeError:
    log_level = logging.INFO
    print(f'Неправильный уровень логирования LOG_LEVEL={LOG_LEVEL}. Используется INFO')

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    filemode='a'
)

# Подставляем токены telebot и pyowm
owm = OWM(OWM_API_KEY, settings.get_owm_config())
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def get_weather(message):
    try:
        city = message.text
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather # type: ignore

        # Получаем статус (описание погоды)
        status = w.detailed_status if hasattr(w, 'detailed_status') else None

        # Получаем и проверяем данные о температуре
        temp_info = w.temperature('celsius')
        if temp_info and "temp" in temp_info and "temp_min" in temp_info and "temp_max" in temp_info:
            temp = temp_info["temp"]
            temp_min = temp_info["temp_min"]
            temp_max = temp_info["temp_max"]
        else:
            temp = None
            temp_min = None
            temp_max = None

        # Получаем и проверяем данные о ветре
        wind_info = w.wind()
        if wind_info and "speed" in wind_info:
            wind_speed = wind_info["speed"]
            if wind_speed < 5:
                wind_speed_status = 'слабый'
            elif 5 <= wind_speed <= 10:
                wind_speed_status = 'умеренный'
            else:
                wind_speed_status = 'сильный'
        else:
            wind_speed = None
            wind_speed_status = "Нет данных о ветре"

        # Получаем и проверяем данные о давлении
        pressure_info = w.barometric_pressure()
        if pressure_info and "sea_level" in pressure_info:
            pressure = pressure_info['sea_level']
            pressure_mm = pressure * 0.750062
            if pressure_mm < 758:
                pressure_status = 'пониженное'
            elif 758 <= pressure_mm <= 762:
                pressure_status = 'нормальное'
            else:
                pressure_status = 'повышенное'
        else:
            pressure_mm = None
            pressure_status = "Нет данных о давлении"

        # Формируем сообщение
        message_text = ''

        if status:
            message_text += f'В <b>{city}е </b> сейчас <b>{status}</b>\n\n'

        if temp is not None:
            message_text += f'🌡Температура: <b>{temp:.1f}°C</b> | '
            if temp_min is not None and temp_max is not None:
                message_text += f'<i>мин. {temp_min:.1f}°C, макс. {temp_max:.1f}°C</i>\n'

        if wind_speed is not None:
            message_text += f'💨Скорость ветра: <b>{wind_speed:.1f} м/с</b> | <i>{wind_speed_status}</i>\n'

        if pressure_mm is not None:
            message_text += f'🏧Давление: <b>{pressure_mm:.1f} мм рт. ст.</b> | <i>{pressure_status}</i>\n'

        if message_text == '':
            message_text = 'К сожалению, погодные данные для этого города недоступны.'

        bot.send_message(message.chat.id, message_text, parse_mode='html')

        logger.info(f'Пользователь {message.from_user.id} ({message.from_user.username}) '
                    f'получил погоду в городе {city}')

    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка {e}')
        bot.send_message(message.chat.id, 'Пожалуйста, попробуйте ввести город еще раз.')
        time.sleep(1)
        logger.info(f'Пользователь {message.from_user.id} ({message.from_user.username}) '
                    f'ввел некоректные данные "{message.text}" с ошибкой "{e}"')
