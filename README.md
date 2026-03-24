# Tg_weather_bot

Telegram-бот для получения актуальной погоды в любом городе России.

🤖 **Попробовать бота:** [https://t.me/Weather131_bot](https://t.me/Weather131_bot)

## О проекте

Бот использует API [OpenWeatherMap](https://openweathermap.org/) для получения погодных данных и предоставляет пользователю:

- 🌡 Текущую температуру (с минимальным и максимальным значением)
- 💨 Скорость и характеристику ветра (слабый / умеренный / сильный)
- 🏧 Атмосферное давление в мм рт. ст. (пониженное / нормальное / повышенное)
- 📋 Подробное описание погодных условий

### Структура проекта

```
Tg_weather_bot/
├── app/
│   ├── core/
│   │   └── config.py        # Конфигурация и переменные окружения
│   ├── keyboards/
│   │   └── keyboards.py     # Reply-клавиатуры бота
│   ├── utils/
│   │   └── weather.py       # Логика получения погоды через OWM
│   ├── logs/
│   │   └── bot.log          # Файл логов
│   └── main.py              # Точка входа, обработчики команд
├── .env.template            # Шаблон файла переменных окружения
├── requirements.txt
└── README.md
```

### Технологии

| Библиотека | Назначение |
|---|---|
| `pyTelegramBotAPI` (`telebot`) | Взаимодействие с Telegram Bot API |
| `pyowm` | Получение погодных данных от OpenWeatherMap |
| `pydantic-settings` | Управление конфигурацией через `.env` |

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/GIT01-byte/Tg_weather_bot
    cd "Tg_weather_bot"
    ```
2. Установите зависимости:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r requirements.txt
    ```

## Настройка

1. Зарегистрируйте бота в Telegram через [BotFather](https://ibot.by/info/base/token/), чтобы получить токен API.
2. Зарегистрируйтесь на [OpenWeatherMap](https://openweathermap.org/), чтобы получить токен API.
3. Создайте файл `.env` в корневой папке проекта (можно скопировать из `.env.template`) и добавьте в него:
    ```
    BOT_TOKEN=ВАШ_ТОКЕН_ИЗ_BOTFATHER
    OWM_API_KEY=ВАШ_ТОКЕН_ИЗ_OWM
    ```

## Запуск

```bash
python .\app\main.py
```

После запуска бот начнёт принимать сообщения. Логи записываются в `app/logs/bot.log`.

## Использование

1. Откройте бота: [https://t.me/Weather131_bot](https://t.me/Weather131_bot)
2. Отправьте команду `/start`
3. Нажмите кнопку **«Узнать погоду»**
4. Введите название города на русском или английском языке
5. Получите актуальный прогноз погоды

## Лицензия

Проект распространяется под лицензией [LICENSE](LICENSE).
