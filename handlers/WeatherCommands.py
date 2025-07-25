from functions.get_weather import get_weather
from markups.weather_text import get_weather_text
import redis
from functions.scheduler_message import send_weather_message
from aiogram import Bot, Router
from asyncio import sleep
from markups.jobs_text import get_job_text
from database.users import get_user, add_jobs, delete_jobs
from markups.error_text import get_weather_error, get_weather_error2
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from apscheduler.jobstores.base import JobLookupError
from datetime import datetime
from zoneinfo import ZoneInfo
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

dp = Router()

@dp.message(Command("weather"))
async def weather(message: Message, bot: Bot, command: CommandObject):
    try:
        args = command.args.split()
    except AttributeError:
        args = [0]
    if len(args) != 2:
        error_text = await get_weather_error2()
        await message.reply(text=error_text)
    else:
        try:
            weather = await get_weather(args[0])
            texting = await get_weather_text(weather)
            await bot.send_message(chat_id=message.from_user.id, text=f"{texting}")
        except KeyError:
            bot_message = await message.answer('⚠️ <b>Введенный город не существует</b>')
            await sleep(5)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await bot_message.delete()

@dp.message(Command("set"))
async def weather(message: Message, bot: Bot, command: CommandObject, scheduler: AsyncIOScheduler):
    try:
        args = command.args.split()
    except AttributeError:
        args = [0]
    if len(args) != 2:
        error_text = await get_weather_error()
        await message.reply(text=error_text)
    else:
        try:
            weather = await get_weather(args[0])
            try:
                time = int(args[1])
                if time<0 or time>23:
                    bot_message = await message.answer("⚠️ <b>Введите правильное время!</b>")
                    await sleep(5)
                    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
                    await bot_message.delete()
                else:
                    user = await get_user(message.from_user.id)
                    tz = ZoneInfo(f"{weather['location']['tz_id']}")
                    city_time = datetime.now(tz)
                    time_difference = int(city_time.utcoffset().total_seconds() / 3600)
                    texing = await get_job_text(time, weather["location"]["name"], time_difference)
                    if time_difference < 0:
                        if int(args[1]) + time_difference < 0:
                            execute_hour = 24 - (int(args[1]) + time_difference) * -1
                        else:
                            execute_hour = int(args[1]) + time_difference
                    else:
                        if int(args[1]) - time_difference < 0:
                            execute_hour = 24 - (time_difference - int(args[1]))
                        else:
                            execute_hour = int(args[1]) - time_difference
                    try:
                        scheduler.remove_job(job_id=user[3])
                    except JobLookupError:
                        logging.info(f'Работа с id {user[3]} не найдена.')
                    except redis.exceptions.DataError:
                        logging.info(f'Работа с id {user[3]} не найдена.')
                    await delete_jobs(message.from_user.id)
                    schedule = scheduler.add_job(send_weather_message, 'cron',
                                                 hour=execute_hour,
                                                 kwargs={'user_id': user[0],'city': args[0]})
                    await message.reply(f"{texing}")
                    await add_jobs(schedule.id, message.from_user.id)
            except IndexError:
                bot_message = await message.answer("⚠️ <b>Введите правильное время!</b>")
                await sleep(5)
                await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
                await bot_message.delete()
        except KeyError:
            bot_message = await message.answer('⚠️ <b>Введенный город не существует</b>')
            await sleep(5)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await bot_message.delete()