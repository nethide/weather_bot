from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router
from markups.start_text import get_start_text
from database.create_database import create_database
from database.users import check_user, insert_user
import logging

dp = Router()

@dp.message(CommandStart())
async def start(message: Message):
    texting = await get_start_text()
    await create_database()
    check = await check_user(message.from_user.id)
    if check is False:
        await insert_user(message.from_user.id)
        logging.info(f'{message.from_user.id} добавлен в базу')
    await message.reply(text=texting)