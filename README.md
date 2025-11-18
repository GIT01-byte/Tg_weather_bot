# Tg_weather_bot
Определи погоду в любом горроде с помощью этого telegramm бота!

## Установка

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/GIT01-byte/Tg_weather_bot
    cd "Tg_weather_bot"
    ```
2.  Установите зависимости:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    pip install -r requirements.txt
    ```
## Настройка

1.  Зарегистрируйте бота в Telegram, используя BotFather https://ibot.by/info/base/token/, чтобы получить токен API.
2.  Зарешистрийтесь на Open Weather Map, используя OWM https://openweathermap.org/, чтобы получить токен API.
3.  Создайте файл `.env` в корневой папке проекта и добавьте в него:
    ```
    BOT_TOKEN=ВАШ_ТОКЕН_ИЗ_BOTFATHER
    OWM_API_KEY=ВАШ_ТОКЕН_ИЗ_OWM
    ```

## Запуск

```bash
python main.py
