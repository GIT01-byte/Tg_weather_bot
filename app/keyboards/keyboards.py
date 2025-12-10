import logging

import telebot
from telebot import types

from core import config

logger = logging.getLogger(__name__)

# Используем значения конфигурации, импортированные из config.py
BOT_TOKEN = config.BOT_TOKEN
OWM_API_KEY = config.OWM_API_KEY
LOG_LEVEL = config.LOG_LEVEL
LOG_FILE_PATH = config.LOG_FILE_PATH

# Настраиваем логирование
try:
    log_level = getattr(logging, config.LOG_LEVEL)
except AttributeError:
    log_level = logging.INFO
    print(f'Неправильный уровень логирования LOG_LEVEL={LOG_LEVEL}. Используется INFO')

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    filemode='a'
)

bot = telebot.TeleBot(BOT_TOKEN)

# Приветственная клавиатура, вызываеться первой
@bot.message_handler(content_types=['text'])
def welcome_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Узнать погоду')
    btn2 = types.KeyboardButton('Настройки')
    btn3 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Нажми на кнопки снизу, чтобы узнать погоду.', reply_markup=markup)


# Вызываеться после получения погоды либо когда произошли ошибки связанные с неккоректным вводом города
@bot.message_handler(content_types=['text'])
def change_city_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Изменить город')
    btn2 = types.KeyboardButton('Вернуться в главное меню')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Что дальше?', reply_markup=markup)
