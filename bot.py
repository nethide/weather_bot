from logging import basicConfig as LoggingConfig
import logging
from asyncio import gather, run
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.client.default import DefaultBotProperties
from middlewares.job_to_handler import SchedulerMiddleware
from aiogram.enums import ParseMode
from config import BOT_TOKEN, USERS

LoggingConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

from handlers.WeatherCommands import dp as weather_router
from handlers.CommandStart import dp as start_souter

async def main():
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.start()
    dp.include_routers(start_souter, weather_router)
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    await dp.start_polling(bot)

if __name__ == '__main__':
    run(main())

    

