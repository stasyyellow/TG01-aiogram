import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
import random
import requests
from config import bot_token, weather_api_key

# Инициализация бота
bot = Bot(token=bot_token)
dp = Dispatcher()

cities = ['Moscow', 'London', 'Paris', 'New York', 'Tokyo', 'Prague', 'Yuma', 'Chicago', 'Warsaw', 'Lisbon', 'Rome', 'Stockholm', 'Berlin']

# Команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот прогноза погоды. Используй команду /weather, чтобы узнать погоду случайного города!")

# Функция для получения прогноза погоды
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = data['weather'][0]['description']
        temp = data['main']['temp']

        return f"Погода в {city}: {weather}, температура: {temp}°C"
    else:
        return "Не удалось получить прогноз погоды."

# Команда /weather
@dp.message(Command('weather'))
async def weather(message: types.Message):
    city = random.sample(cities, 1)[0]  # Выбираем случайный город
    weather_report = get_weather(city)  # Получаем прогноз погоды
    await message.answer(weather_report)

# Команда /help
@dp.message(Command('help'))
async def help(message: types.Message):
    await message.answer("Доступные команды:\n/start - Начать\n/weather - Узнать погоду\n/help - Помощь")


# Асинхронный запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
