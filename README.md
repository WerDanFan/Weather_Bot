# Weather Forecasts

Weather Forecasts — это Telegram-бот для получения прогноза погоды для нескольких городов. Бот поддерживает выбор временного интервала прогноза, обработку нескольких точек маршрута и предоставление информации о температуре, влажности, ветре и вероятности осадков.

## Функциональность

- **/start** — Приветствие и краткое описание возможностей бота.
- **/help** — Список доступных команд и инструкции по использованию бота.
- **/weather** — Получение прогноза погоды.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/eshevlyakova/forecasts-for-trips-bot.git
    ```

2. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

3. Введите токен от своего бота

    - **BOT_TOKEN** — это токен вашего бота в Telegram. Его можно получить через BotFather в Telegram.
    - 
4. Запустите бота:

    ```bash
    python bot.py
    ```

## Использование

1. После запуска бота в Telegram, отправьте команду `/start`, чтобы начать использование бота.
2. Для получения прогноза погоды, введите название городов для прогноза, выберите временной промежуток для прогноза, затем введите /weather или нажмите "Получить прогноз погоды" 
3. Бот предоставит прогноз погоды для каждого города на маршруте, включая температуру, влажность, ветер и вероятность осадков.