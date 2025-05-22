import os

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import message, Message

from dotenv import load_dotenv, find_dotenv
from .database import (
                    Session,
                    UserAnime,
                    User,
                    Anime,
                    up,
                    drop) 

load_dotenv(find_dotenv())

async def main():
    bot = Bot(os.getenv('TOKEN'))
    dp = Dispatcher()
    up()

    await dp.start_polling(bot)
