import logging
from asyncio import sleep
from datetime import datetime
from zoneinfo import ZoneInfo

import redis
from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.users import get_user, add_jobs, delete_jobs
from functions.get_weather import get_weather
from functions.scheduler_message import send_weather_message
from markups.jobs_text import get_job_text
from markups.weather_text import get_weather_text

dp = Router()

class WaitWeather(StatesGroup):
    city = State()
    message_id = State()

class SetWeather(StatesGroup):
    city = State()
    time = State()
    message_id = State()
    weather = State()

@dp.message(Command("weather"))
async def weather(message: Message, state: FSMContext):
    message_to_save = await message.reply(text="<b>ℹ️ Введите город:</b>")
    await state.set_state(WaitWeather.city)
    await state.update_data(message_id=message_to_save.message_id)

@dp.message(WaitWeather.city)
async def send_weather(message: Message, bot: Bot, state: FSMContext):
    get = await state.get_data()
    message_to_edit = int(get['message_id'])
    try:
        await message.delete()
        current_weather = await get_weather(message.text)
        texting = await get_weather_text(current_weather)
        await bot.edit_message_text(message_id=message_to_edit,
                                    chat_id=message.from_user.id,
                                    text=f"{texting}")
        await state.clear()
    except KeyError:
        await bot.edit_message_text(message_id=message_to_edit,
                                    chat_id=message.from_user.id,
                                    text='⚠️ <b>Введенный город не существует</b>\r \r'
                                        f'<blockquote>{message.text}</blockquote> '
                                        f'Попробуйте еще.')


@dp.message(Command("set"))
async def set(message: Message, state: FSMContext):
    message_to_edit = await message.reply(f"Отлично, приступим✨ \r \n<b>Введите город:</b>")
    await state.set_state(SetWeather.city)
    await state.update_data(message_id=message_to_edit.message_id)

@dp.message(SetWeather.city)
async def set_city(message: Message, state: FSMContext, bot: Bot):
    get = await state.get_data()
    message_to_edit = int(get['message_id'])
    try:
        current_weather = await get_weather(message.text)
        city = current_weather["location"]["name"]
        country = current_weather["location"]["country"]
        await state.update_data(city=message.text)
        await state.clear()
        await message.delete()
        await bot.edit_message_text(message_id=message_to_edit,
                                    chat_id=message.from_user.id,
                                    text=f"<b>✅ Установлен город {city}, {country}</b> \r \n"
                                            "Теперь введи время, в которое хочешь получать погоду."
                                            "<blockquote>Примеры: \r \n"
                                            "8:30, 11:12</blockquote>"
                                            "<i>Поправка на часовой пояс города - автоматическая</i>")
        await state.set_state(SetWeather.time)
        await state.update_data(message_id=message_to_edit, weather=current_weather)
    except KeyError:
        await bot.edit_message_text(message_id=message_to_edit,
                                    chat_id=message.from_user.id,
                                    text='⚠️ <b>Введенный город не существует</b>\r \r'
                                        f'<blockquote>{message.text}</blockquote> '
                                        f'Попробуйте еще.')
        await message.delete()

@dp.message(SetWeather.time)
async def set_weather(message: Message, bot: Bot, state: FSMContext, scheduler: AsyncIOScheduler):
    get = await state.get_data()
    message_to_edit = int(get['message_id'])
    parts = message.text.split(':')
    if len(parts) != 2:
        msg = (f"<b>Ошибка ⚠️</b> \r \n"
               f"Используйте формат HH:MM!")
    else:
        try:
            hour = int(parts[0])
            minutes = int(parts[1])

            if hour < 0 or hour > 23:
                msg = (f"Ошибка ⚠️ \r \n"
                       f"Часы должны быть от 0 до 23 \r \n"
                       f"<i>Попробуйте еще.</i>")
            elif minutes <0 or minutes > 59:
                msg = (f"Ошибка ⚠️ \r \n"
                       f"Минуты должны быть от 0 до 59 \r \n"
                       f"<i>Попробуйте еще.</i>")
            else:
                city_weather = get['weather']
                user = await get_user(message.from_user.id)
                tz = ZoneInfo(f"{city_weather['location']['tz_id']}")
                city_time = datetime.now(tz)
                time_difference = int(city_time.utcoffset().total_seconds() / 3600)
                texing = await get_job_text(f"{parts[0]}:{parts[1]}", city_weather["location"]["name"], time_difference)
                if time_difference < 0:
                    if int(hour) + time_difference < 0:
                        execute_hour = 24 - (int(hour) + time_difference) * -1
                    else:
                        execute_hour = int(hour) + time_difference
                else:
                    if int(hour) - time_difference < 0:
                        execute_hour = 24 - (time_difference - int(hour))
                    else:
                        execute_hour = int(hour) - time_difference
                try:
                    scheduler.remove_job(job_id=user[3])
                except JobLookupError:
                    logging.info(f'Работа с id {user[3]} не найдена.')
                except redis.exceptions.DataError:
                    logging.info(f'Работа с id {user[3]} не найдена.')
                await delete_jobs(message.from_user.id)
                schedule = scheduler.add_job(send_weather_message, 'cron',
                                             hour=execute_hour,
                                             minute=minutes,
                                             kwargs={'user_id': user[0], 'city': city_weather["location"]["name"]})
                await add_jobs(schedule.id, message.from_user.id)
                msg = texing
        except ValueError:
            msg = (f"Ошибка ⚠️ \r \n"
                   f"Принимаются только числа!\r \n"
                   f"<i>Попробуйте еще.</i>")
    await message.delete()
    await bot.edit_message_text(text=f"{msg}", message_id=message_to_edit, chat_id=message.from_user.id)



"""except IndexError:
            bot_message = await message.answer("⚠️ <b>Введите правильное время!</b>")
            await sleep(5)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await bot_message.delete()
    except KeyError:
        bot_message = await message.answer('⚠️ <b>Введенный город не существует</b>')
        await sleep(5)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await bot_message.delete()"""