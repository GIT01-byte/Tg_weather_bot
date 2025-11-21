from datetime import datetime
import logging

import telebot

from core import config
from keyboards.keyboards import welcome_keyboard, change_city_keyboard
from utils.weather import get_weather

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
    filemode='a' # для добавления записей
)

# Создаем экземпляр Бота с токеном на Telebot, для работы с ним и Telegram
bot = telebot.TeleBot(BOT_TOKEN)

logging.info(f'Бот запущен: {datetime.now()}')

@bot.message_handler(commands=['start'])
def welcome(message):
    """Обработчик команды /start."""
    try:
        bot.send_message(
            message.chat.id,
            f'Добро пожаловать {message.from_user.first_name} {message.from_user.last_name}! '
            f'Я погодный бот.',
            parse_mode='html'
            )
        logger.info(f"Пользователь {message.from_user.id} ({message.from_user.username}) запустил бота")
        # Инициализируем приветственную клавиатуру и сам блок клавиатур вобщем
        welcome_keyboard(message)
    except Exception as e:
        logger.exception(f'Ошибка в функции welcome для пользователя {message.from_user.id}: {e}')


# Обработчики Reply кнопок
@bot.message_handler(func=lambda message: message.text == 'Узнать погоду')
def ask_for_city(message):
    """Запрашивает у пользователя город."""
    logger.info(f'Пользователь {message.from_user.id} ({message.from_user.username}) '
                f'воспользовался кнопкой {message.text}')
    bot.send_message(message.chat.id, 'Введите ваш город:')
    # После отправки сообщения регистсрируем обработчик для получения погоды
    bot.register_next_step_handler(message, get_weather_handler)

# Обработчик для вызова функция для получения погоды
def get_weather_handler(message):
    """Получает погоду для введенного города и отправляет ее пользователю."""
    city = message.text
    try:
        get_weather(message) # получаем сведения о погоде
        change_city_keyboard(message) # переходим к клавиатуре для смены города
    except Exception as e:
        logger.exception(f'Ошибка при получении погоды в городе {city}: {e}')
        bot.reply_to(message, "Произошла ошибка при получении погоды. Попробуйте еще раз.")


@bot.message_handler(func=lambda message: message.text == 'Помощь')
def get_help(message):
    """Обработчик для кнопки 'Помощь'."""
    logger.info(f'Пользователь {message.from_user.id} ({message.from_user.username}) '
                f'воспользовался кнопкой {message.text}')
    bot.send_message(message.chat.id, 'Я пока что реализовываю эту функцию...')
    welcome_keyboard(message)

@bot.message_handler(func=lambda message: message.text == 'Настройки')
def get_settings(message):
    """Обработчик для кнопки 'Настройки'."""
    logger.info(f'Пользователь {message.from_user.id} ({message.from_user.username}) '
                f'воспользовался кнопкой {message.text}')
    bot.send_message(message.chat.id, 'Я пока что реализовываю эту функцию...')
    welcome_keyboard(message)


@bot.message_handler(func=lambda message: message.text == 'Изменить город')
def ask_for_city_handler(message):
    logger.info(f'Пользователь {message.from_user.id} ({message.from_user.username}) '
                f'воспользовался кнопкой {message.text}')
    ask_for_city(message)

@bot.message_handler(func=lambda message: message.text == 'Вернуться в главное меню')
def return_to_main_menu_handler(message):
    logger.info(f'Пользователь {message.from_user.id} ({message.from_user.username}) '
                f'воспользовался кнопкой {message.text}')
    welcome_keyboard(message)


# Обрабатываем прочие команды
@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Обработчик для текстовых сообщений, не являющихся командами или кнопками."""
    if message.text in button_actions:
        button_actions[message.text](message)
    else:
        bot.send_message(message.chat.id, "Я не понимаю эту команду.  Нажмите на одну из кнопок.")
        welcome_keyboard(message)


# Словарь для вызова функций по тексту сообщений
button_actions = {
    'Изменить город': ask_for_city,
    'Узнать погоду': get_weather,
    'Помощь': get_help,
    'Настройки': get_settings,
    'Вернуться в главное меню': welcome_keyboard
}

# Запускаем Бота в вечном режиме
bot.infinity_polling()
