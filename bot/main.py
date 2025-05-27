import os

from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import message, Message
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from dotenv import load_dotenv, find_dotenv
from .database import (
                    Session,
                    UserAnime,
                    User,
                    Anime,
                    up,
                    drop,
                    engine) 

from .keyboards.reply import main_menu
from .handlers import config_handler, library_handler
from .utils import UserState

load_dotenv(find_dotenv())

dp = Dispatcher()

@dp.message(CommandStart())
async def give_main_menu(message: Message, state: FSMContext):

    user_id = message.from_user.id

    try:

        async with Session.begin() as session:
            user = await session.scalar(select(User).filter(User.id == user_id))
            if not user:
                session.add(User(id = user_id))
                await session.flush()
                await message.answer(f'Welcome! {message.from_user.first_name}.', reply_markup=main_menu())
                await state.set_state(UserState.user_action)

            else:
                await message.answer(f'Hello! {message.from_user.first_name}', reply_markup=main_menu())
                await state.set_state(UserState.user_action)

    except Exception as e:
        print(e)
        await message.answer('Error!')

async def main():
    bot = Bot(os.getenv('TOKEN'))
    await drop(async_engine=engine)
    await up(async_engine=engine)


    dp.include_routers(
        config_handler,
        library_handler
                    )

    await dp.start_polling(bot)
