#импорт необходимых библиотек
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
import asyncio
import requests
from weather import Weather
from message_forecast import forecasts

# Настройка логирования
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = '' #Введите свой ключ api

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь для хранения пользователей
user_data = {}

# Множество запрещенных для ввода символов
BAD_SYMBOLS = {'1','2','3','4','5','6','7','8','9','!','?',',','.','/','(',')','*','@','#','$',"'",'+','_'}

### --- ОБРАБОТЧИК КОМАНД ---
@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    if F.text == '/start':
        user_data[message.from_user.id] = {'cities': set(), 'days': -1}
    # Создаём кнопки
    button_about = KeyboardButton(text='Помощь')
    button_add_city = KeyboardButton(text='Добавить город')
    button_remove_city = KeyboardButton(text='Удалить город')
    button_choose_days = KeyboardButton(text='Выбрать время')
    button_get_weather = KeyboardButton(text='Получить прогноз погоды')

    # Создаём клавиатуру и добавляем кнопки
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_add_city, button_remove_city],
                  [button_choose_days,button_about],
                  [button_get_weather]],
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

    await message.answer(
        'Привет! Я бот для просмотра погоды. \n'
        'Добавь город, выбери промежуток времени и нажми "Получить прогноз погоды"',
        reply_markup=reply_keyboard,
    )

@dp.message(F.text == 'Вернуться в главное меню')
async def back_to_start_command(message: types.Message):
    # Создаём кнопки
    button_about = KeyboardButton(text='Помощь')
    button_add_city = KeyboardButton(text='Добавить город')
    button_remove_city = KeyboardButton(text='Удалить город')
    button_choose_days = KeyboardButton(text='Выбрать время')
    button_get_weather = KeyboardButton(text='Получить прогноз погоды')

    # Создаём клавиатуру и добавляем кнопки
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_add_city, button_remove_city],
                  [button_choose_days,button_about],
                  [button_get_weather]],
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

    await message.answer(
        'Привет! Я бот для просмотра погоды. \n'
        'Добавь город, выбери промежуток времени и нажми "Получить прогноз погоды"',
        reply_markup=reply_keyboard,
    )

@dp.message(F.text.in_([ 'Помощь', '/help' ]))
async def help_command(message: types.Message):
    await message.answer(
        'Список доступных команд:\n'
        '/start - Начать работу с ботом\n'
        '/help - Получить помощь\n'
        '/weather - Получить прогноз погоды\n'
    )

@dp.message(F.text == 'Добавить город')
async def add_cities(message: types.Message):
    # Создаём кнопки
    button_moscow = KeyboardButton(text='Москва')
    button_tyumen = KeyboardButton(text='Тюмень')
    button_my_geo = KeyboardButton(text="Геолокация", request_location=True)
    button_another = KeyboardButton(text='Другой')
    button_choose_days = KeyboardButton(text='Выбрать время')
    button_main = KeyboardButton(text='Вернуться в главное меню')

    # Создаём клавиатуру и добавляем кнопки
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_tyumen, button_moscow],
                  [button_my_geo, button_another],
                  [button_choose_days],
                  [button_main]],
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

    await message.answer(
        'Выбери один из предложенных городов, отправь геолокацию или введи свой город',
        reply_markup=reply_keyboard,
    )

@dp.message(F.text == 'Удалить город')
async def remove_cities(message: types.Message):
    await message.answer('Чтобы удалить город введите команду \n/remove Москва,Лондон,...')

@dp.message(F.location)
async def geolocation(message: types.Message):
    headers = {'User-Agent': 'Custom Agent'}
    geo = {'format': 'json', 'lat': f'{message.location.latitude}', 'lon': f'{message.location.longitude}'}
    r = requests.get('https://nominatim.openstreetmap.org/reverse', params=geo, headers=headers)
    location = r.json()
    city_name = location["address"]["city"]
    user_data[message.from_user.id]["cities"].add(city_name)
    await message.answer(f'Город "{city_name}" успешно добавлен в прогноз')
    await message.answer(f'Города в прогнозе: {user_data[message.from_user.id]["cities"]}')


@dp.message(F.text == 'Другой')
async def another_city(message: types.Message):
    await message.answer('Чтобы ввести другой город введите команду /add Москва,Лондон,... ')

@dp.message(F.text.startswith('/add'))
async def add_city(message: types.Message):
    # Извлекаем параметр после команды
    cities = message.text.split('/add', 1)[1].strip()
    cities = cities.split(',')
    cities = [city.title() for city in cities if (len(set(city)&BAD_SYMBOLS)==0 and len(city)>0 and len(city)<200)]
    if cities:
        user_data[message.from_user.id]['cities'].update(cities)
        await message.answer(f'Город(a) {cities} добавлены в прогноз')
        await message.answer(f'Города в прогнозе: {user_data[message.from_user.id]["cities"]}')
    else:
        await message.answer(f'Некорректный ввод. Попробуйте еще раз.')

@dp.message(F.text.startswith('/remove'))
async def remove_city(message: types.Message):
    # Извлекаем параметр после команды
    cities = message.text.split('/remove', 1)[1].strip()
    cities = cities.split(',')
    cities = [city.title() for city in cities if str(city).isalpha()]
    for city in cities:
        user_data[message.from_user.id]['cities'].discard(city)
    await message.answer(f'Удаление произведено')
    await message.answer(f'Города в прогнозе: {user_data[message.from_user.id]["cities"]}')


@dp.message(F.text == 'Тюмень')
async def tyumen_city(message: types.Message):
    user_data[message.from_user.id]['cities'].add('Тюмень')
    await message.answer(f'Город Тюмень добавлен в прогноз')
    await message.answer(f'Города в прогнозе: {user_data[message.from_user.id]["cities"]}')

@dp.message(F.text == 'Москва')
async def moscow_city(message: types.Message):
    user_data[message.from_user.id]['cities'].add('Москва')
    await message.answer(f'Город Москва добавлен в прогноз')
    await message.answer(f'Города в прогнозе: {user_data[message.from_user.id]["cities"]}')


@dp.message(F.text == 'Выбрать время')
async def choose_time(message: types.Message):
    # Создаём кнопки
    button_1_day = KeyboardButton(text='Прогноз на 1 день')
    button_3_day= KeyboardButton(text='Прогноз на 3 дня')
    button_5_day = KeyboardButton(text="Прогноз на 5 дней")
    button_main = KeyboardButton(text='Вернуться в главное меню')
    button_get_weather = KeyboardButton(text='Получить прогноз погоды')

    # Создаём клавиатуру и добавляем кнопки
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1_day, button_3_day, button_5_day],
                  [button_get_weather],
                  [button_main]],
        resize_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )

    await message.answer(
        'Выбери сколько дней будет в прогнозе',
        reply_markup=reply_keyboard,
    )

@dp.message(F.text == 'Прогноз на 1 день')
async def day_1_forecast(message: types.Message):
    user_data[message.from_user.id]['days'] = 0
    await message.answer(f'Выбран "Прогноз на 1 день"')

@dp.message(F.text == 'Прогноз на 3 дня')
async def day_3_forecast(message: types.Message):
    user_data[message.from_user.id]['days'] = 2
    await message.answer(f'Выбран "Прогноз на 3 дня"')

@dp.message(F.text == 'Прогноз на 5 дней')
async def day_5_forecast(message: types.Message):
    user_data[message.from_user.id]['days'] = 4
    await message.answer(f'Выбран "Прогноз на 5 дней"')


@dp.message(F.text == 'Получить прогноз погоды')
async def take_forecast(message: types.Message):
    if len(user_data[message.from_user.id]['cities']) == 0:
        await message.answer('Ошибка! Сначала выберите города, которые будут в прогнозе')
    if user_data[message.from_user.id]['days'] == -1:
        await message.answer('Ошибка! Сначала выберите промежуток времени для прогноза погоды')

    if len(user_data[message.from_user.id]['cities']) != 0 and user_data[message.from_user.id]['days'] != -1:
        await message.answer(f'Идет процесс получения прогноза погоды на {user_data[message.from_user.id]['days']+1} дней '
                            f'для следующих городов: {user_data[message.from_user.id]['cities']}\n'
                            f'Пожалуйста подождите...')

        error, data = weather.get_df(user_data[message.from_user.id]['cities'])
        if not error:
            for city in list(user_data[message.from_user.id]['cities']):
                await message.answer(forecasts(city,data,user_data[message.from_user.id]['days']))

        else:
            await message.answer(data)
            if 'Пожалуйста повторите ввод.' in data:
                user_data[message.from_user.id]['cities'] = set()



### --- НЕОБРАБОТАННЫЕ СООБЩЕНИЯ ---
@dp.message()
async def handle_unrecognized_message(message: types.Message):
    await message.answer('Извините, я не понял ваш запрос. Попробуйте использовать команды или кнопки.')


# Запуск бота
if __name__ == '__main__':
    weather = Weather()
    try:
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logging.error(f'Ошибка при запуске бота: {e}')