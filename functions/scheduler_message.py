from aiogram import Bot
from datetime import datetime
from functions.get_weather import get_weather
from markups.weather_text import get_weather_text_schedule

async def send_weather_message(user_id, city, bot: Bot):
    date = datetime.now().strftime("%m-%d-%Y")
    weather = await get_weather(city)
    texting = await get_weather_text_schedule(weather, date)
    await bot.send_message(chat_id=user_id, text=f"{texting}")