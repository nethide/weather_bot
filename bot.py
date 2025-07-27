import logging
from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from config import BOT_TOKEN
from middlewares.job_to_handler import SchedulerMiddleware

logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler('py.log'),
    logging.StreamHandler()
])
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

from handlers.WeatherCommands import dp as weather_router
from handlers.CommandStart import dp as start_souter

async def main():
    jobstores = {
        'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                 run_times_key='dispatched_trips_running',
                                 db=2,
                                 port=6379)
    }
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone="UTC", jobstores=jobstores))
    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()
    dp.include_routers(start_souter, weather_router)
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        logging.info('Bot power off')

    

