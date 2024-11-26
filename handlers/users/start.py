from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta
from aiogram.dispatcher.filters.state import State, StatesGroup

from data.config import ADMINS
from loader import db, dp, bot



# add database  new user
@dp.message_handler(commands='start')
async def message_start(message:types.Message):
    try:
        telegram_id=message.from_user.id
        username=message.from_user.username
        full_name=message.from_user.full_name
        if not db.get_user(telegram_id=telegram_id):
            db.add_user(telegram_id,username,full_name)
            await bot.send_message(ADMINS[0],"Yangi foydalanuvchi qo'shildi ")
        await message.answer("Xush kelibsiz ")


    except Exception as err:
        print(err)
