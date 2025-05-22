import os

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import message, Message

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

async def main():
    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()

    await dp.start_polling(bot)
