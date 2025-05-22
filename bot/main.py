import os

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import message, Message

from sqlalchemy import select

from dotenv import load_dotenv, find_dotenv
from .database import (
                    Session,
                    UserAnime,
                    User,
                    Anime,
                    up,
                    drop) 

load_dotenv(find_dotenv())

dp = Dispatcher()

@dp.message(CommandStart())
async def give_main_menu(message: Message):

    user_id = message.from_user.id

    try:

        with Session.begin() as session:
            user = session.scalar(select(User).filter(User.id == user_id))
            if not user:
                session.add(User(id = user_id))
                session.flush()
                await message.answer(f'Welcome! {message.from_user.first_name}.')

            else:
                await message.answer(f'Hello! {message.from_user.first_name}')

    except Exception as e:
        print(e)
        await message.answer('Error!')

async def main():
    bot = Bot(os.getenv('TOKEN'))
    drop()
    up()

    await dp.start_polling(bot)
