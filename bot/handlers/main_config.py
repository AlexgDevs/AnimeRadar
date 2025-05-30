import asyncio
from typing import Union
from aiogram.types import message, Message, CallbackQuery, InputMediaPhoto
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from sqlalchemy import func, select
from ..API.aiohttp_session import search_anime_title
from ..database import Anime, Session, User, UserAnime

from ..utils import UserState, QueryAnime
from ..keyboards import (
    main_menu,
    library_menu,
    stop_search_button,
    anime_inline_buttons
)

config_handler = Router()

@config_handler.message(F.text == '📚 My Library', UserState.user_action)
async def create_transitions(message: Message, state: FSMContext):

    await message.answer('You select library menu!', reply_markup=library_menu())



@config_handler.message(F.text == '🔙 Back', UserState.user_action)
async def back_to_main_menu(message: Message, state: FSMContext):

    await message.answer('Your back to main menu!', reply_markup=main_menu())


@ config_handler.message(F.text=='Stop', QueryAnime.await_anime_query)
async def stop_search_query(message:Message, state: FSMContext):

    await message.answer('Your stopped search anime!', reply_markup=main_menu())

    await state.clear()
    await state.set_state(UserState.user_action)


@config_handler.message(F.text == '🔍 Search Anime', UserState.user_action)
async def get_query(message: Message, state: FSMContext):

    await message.answer('Введите название аниме', reply_markup=stop_search_button())
    await state.set_state(QueryAnime.await_anime_query)



@config_handler.message(F.text, QueryAnime.await_anime_query)
async def get_current_anime(message: Message, state: FSMContext):

    query = message.text
    current_index = 0
    anime_list = await search_anime_title(query)

    async with Session.begin() as session:
        filtered_anime_list = [
        anime for anime in anime_list
        if anime['mal_id'] is not None
        and anime['title'] is not None
        and anime['episodes'] is not None
        and anime['image_url'] is not None
        and anime['synopsis'] is not None
    ]

        existing_ids = await session.scalars(select(Anime.mal_id))
        existing_ids = set(existing_ids.all())

        for anime in filtered_anime_list:
            if anime['mal_id'] not in existing_ids:
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
        builder.button(text='Предыдущий', callback_data=f'prev_{current_index - 1}_{count}')
    
    if current_index < count - 1:
        button_count += 1
        builder.button(text='Дальше', callback_data=f'next_{current_index + 1}_{count}')

    builder.button(text='Посмотреть', callback_data=f'check_bunner_{current_anime['mal_id']}_{current_index}_{count}')

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
        builder.button(text='Предыдущий', callback_data=f'prev_{current_index - 1}_{count}')
    
    if current_index < count - 1:
        button_count += 1
        builder.button(text='Дальше', callback_data=f'next_{current_index + 1}_{count}')

    builder.button(text='Посмотреть', callback_data=f'check_bunner_{current_anime['mal_id']}_{current_index}_{count}')

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



#check bunner
@config_handler.callback_query(F.data.startswith('check_bunner_'))
async def check_bunner(callback: CallbackQuery):

    await callback.answer()
    mal_id, current_index, count = callback.data.split('_')[2:]


    async with Session() as session:
        current_anime = await session.scalar(select(Anime).filter(Anime.mal_id == mal_id))

        if current_anime:
            caption = f'Titel: {current_anime.title}\n\n{current_anime.synopsis[:200]}'
            await callback.message.edit_media(media=InputMediaPhoto(media=current_anime.photo_url, caption=caption), reply_markup=anime_inline_buttons(mal_id, current_index, count))



# add anime
@config_handler.callback_query(F.data.startswith('add_to_library_'))
async def add_to_library(callback: CallbackQuery):

    await callback.answer()
    mal_id = callback.data.split('_')[3]
    user_id = callback.from_user.id 

    async with Session.begin() as session:
        current_anime = await session.scalar(select(Anime).filter(Anime.mal_id==mal_id))
        user = await session.scalar(select(User).filter(User.id==user_id))

        user_library = await session.scalar(select(UserAnime).filter(UserAnime.user_id==user_id, UserAnime.anime_id==current_anime.id))

        if current_anime and user:
            if not user_library:
                session.add(UserAnime(user=user, anime=current_anime, mal_id=current_anime.mal_id))
                await session.flush()
                await callback.message.answer('Аниме успешно добавлено в вашу библиотеку!')
                
            
            else:
                await callback.message.reply('Текущее аниме находится в вашей библиотеке')
        else:
            await callback.answer('Текущий пользователь или аниме не найдены')



#back to current anime
@config_handler.callback_query(F.data.startswith('back_anime_'))
async def back_to_current_anime(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    anime_list = data.get('anime_list')
    
    mal_id, current_index, count = callback.data.split('_')[2:]

    current_index = int(current_index)
    count = int(count)

    current_anime = anime_list[current_index]

    button_count = 0

    builder = InlineKeyboardBuilder()
    if current_index > 0:
        button_count += 1
        builder.button(text='Предыдущий', callback_data=f'prev_{current_index - 1}_{count}')
    
    if current_index < count - 1:
        button_count += 1
        builder.button(text='Дальше', callback_data=f'next_{current_index + 1}_{count}')

    builder.button(text='Посмотреть', callback_data=f'check_bunner_{current_anime['mal_id']}')

    if button_count == 2:
        choice = builder.adjust(2, 1).as_markup()

    else:
        choice = builder.adjust(1).as_markup()

    caption = f'Titel: {current_anime['title']}\n\n{current_anime['synopsis'][:200]}\n\nPage {current_index + 1} | {count}'
    await callback.message.edit_media(media=InputMediaPhoto(media=current_anime['image_url'], caption=caption), reply_markup=choice)



