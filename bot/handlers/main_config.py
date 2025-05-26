import asyncio
from typing import Union
from aiogram.types import message, Message, CallbackQuery, InputMediaPhoto
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from sqlalchemy import func, select
from ..API.aiohttp_session import search_anime_title
from ..database import Anime, Session

from ..utils import UserState, QueryAnime
from ..keyboards import (
    main_menu,
    library_menu,
)

config_handler = Router()

@config_handler.message(F.text == '📚 My Library', UserState.user_action)
async def create_transitions(message: Message, state: FSMContext):

    await message.answer('You selected library menu!', reply_markup=library_menu())

@config_handler.message(F.text == '🔙 Back', UserState.user_action)
async def back_to_main_menu(message: Message, state: FSMContext):

    await message.answer('You back to main menu!', reply_markup=main_menu())


@config_handler.message(F.text == '🔍 Search Anime', UserState.user_action)
async def get_query(message: Message, state: FSMContext):

    await message.answer('Введите название аниме')
    await state.set_state(QueryAnime.await_anime_query)


@config_handler.message(F.text, QueryAnime.await_anime_query)
async def get_current_anime(message: Message, state: FSMContext):

    query = message.text
    current_index = 0
    anime_list = await search_anime_title(query)

    async with Session.begin() as session:
        
        exiting = await session.scalars(select(Anime))
        result = exiting.all()

        filtered_anime_list = [
            anime for anime in anime_list
            if anime['mal_id'] is not None
            and anime['title'] is not None
            and anime['episodes'] is not None
            and anime['image_url'] is not None
            and anime['synopsis'] is not None
        ]
        # какой колхоз ахахаха, ну пока так, хуйня генератор кнч ну да пофек, главное что корутина возврощает не None

        if not result:
            for anime in filtered_anime_list:

                    session.add(Anime(
                        mal_id=anime['mal_id'],
                        title=anime['title'],
                        last_episode=anime['episodes'],
                        photo_url=anime['image_url'],
                        synopsis=anime['synopsis']
                    ))
                    await session.flush()

    await state.update_data(anime_list=anime_list)
    await show_current_anime(message=message, current_index=current_index, anime_list=anime_list)



async def show_current_anime(message: Message, current_index: int, anime_list: dict):

    current_anime = anime_list[current_index]
    count = len(anime_list)


    button_count = 0
    builder = InlineKeyboardBuilder()
    if current_index > 0:
        button_count += 1
        builder.button(text='back', callback_data=f'prev_{current_index - 1}_{count}')
    
    if current_index < count - 1:
        button_count += 1
        builder.button(text='next', callback_data=f'next_{current_index + 1}_{count}')

    builder.button(text='Add in my library', callback_data=f'buy_{current_anime['mal_id']}')

    if button_count == 2:
        choice = builder.adjust(2, 1).as_markup()

    else:
        choice = builder.adjust(1).as_markup()

    caption = f'Titel: {current_anime['title']}\n\n{current_anime['synopsis'][:200]}\n\nPage {current_index + 1} | {count}'
    await message.answer_photo(photo=current_anime['image_url'], caption=caption, reply_markup=choice)



async def get_current_page(callback: CallbackQuery, state: FSMContext):
    
    await callback.answer()
    data = await state.get_data()
    anime_list = data.get('anime_list')

    current_index, count = callback.data.split('_')[1:]
    
    current_index = int(current_index)
    count = int(count)

    current_anime = anime_list[current_index]

    button_count = 0

    builder = InlineKeyboardBuilder()
    if current_index > 0:
        button_count += 1
        builder.button(text='back', callback_data=f'prev_{current_index - 1}_{count}')
    
    if current_index < count - 1:
        button_count += 1
        builder.button(text='next', callback_data=f'next_{current_index + 1}_{count}')

    builder.button(text='Add in my library', callback_data=f'buy_{current_anime['mal_id']}')

    if button_count == 2:
        choice = builder.adjust(2, 1).as_markup()

    else:
        choice = builder.adjust(1).as_markup()

    caption = f'Titel: {current_anime['title']}\n\n{current_anime['synopsis'][:200]}\n\nPage {current_index + 1} | {count}'
    await callback.message.edit_media(media=InputMediaPhoto(media=current_anime['image_url'], caption=caption), reply_markup=choice)



@config_handler.callback_query(F.data.startswith('next_'))
async def next_current_page(callback: CallbackQuery, state: FSMContext):
    await get_current_page(callback, state)



@config_handler.callback_query(F.data.startswith('prev_'))
async def back_current_page(callback: CallbackQuery, state: FSMContext):
    await get_current_page(callback, state)















