import math
from typing import Union
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InputMediaPhoto, Message, CallbackQuery
from sqlalchemy import func, select
from ..database import Session, Anime

async def index_pagination(message, current_index, anime_list):

    try:

        count = len(anime_list)
        current_anime = anime_list[current_index]
        
        prev_next_builder = InlineKeyboardBuilder()
        total_button = 0

        if current_index < count - 1:
            prev_next_builder.button(text='⭢', callback_data=f'next_{current_index + 1}_{count}')
            total_button += 1
        
        if current_index > 1:
            prev_next_builder.button(text='⭠', callback_data=f'prev_{current_index - 1}_{count}')
            total_button += 1

        prev_next_builder.button(text='Подробней', callback_data=f'mal_id_current_anime:{current_anime['mal_id']}:{count}:{current_index}')
        if total_button == 2:
            scroll_menu = prev_next_builder.adjust(2, 1).as_markup()
        else:
            scroll_menu = prev_next_builder.adjust(1, 1).as_markup()

        await message.answer_photo(photo=current_anime['image'], caption=f'Название: {current_anime['title']}\n\nСтраница {current_index + 1} из {count}', reply_markup=scroll_menu)

    except Exception as e:
        await message.answer('Данные устарели, введите название еще раз')
        print(e)

async def shift_index(callback, state):

    try:
            
        await callback.answer()
        data = await state.get_data()
        anime_list = data.get('anime_list')

        current_index, count = callback.data.split('_')[1:]

        current_index = int(current_index)
        count = int(count)

        current_anime = anime_list[current_index]

        prev_next_builder = InlineKeyboardBuilder()
        total_button = 0

        if current_index > 0:
            prev_next_builder.button(text='⭠', callback_data=f'prev_{current_index - 1}_{count}')
            total_button += 1

        if current_index < count - 1:
            prev_next_builder.button(text='⭢', callback_data=f'next_{current_index + 1}_{count}')
            total_button += 1
            
        prev_next_builder.button(text='Подробней', callback_data=f'mal_id_current_anime:{current_anime['mal_id']}:{count}:{current_index}')
        if total_button == 2:
            scroll_menu = prev_next_builder.adjust(2, 1).as_markup()
        else:
            scroll_menu = prev_next_builder.adjust(1, 1).as_markup()

        await callback.message.edit_media(media=InputMediaPhoto(media=current_anime['image'], caption=f'Название: {current_anime['title']}\n\nСтраница {current_index + 1} из {count}'), reply_markup=scroll_menu)

    except Exception as e:
        await callback.message.answer('Данные устарели, введите название еще раз')
        print(e)



async def deafult_pagination(message: Message, current_page: int):
    async with Session() as session:
        count = await session.scalar(select(func.count(Anime.mal_id)))
        total_pages = math.ceil(count / 10)
        offset = (current_page - 1) * 10

        current_animes = await session.scalars(select(Anime).offset(offset).limit(10))
        animes = current_animes.all()

        if animes:
            builder = InlineKeyboardBuilder()
            for anime in animes:
                builder.button(text=anime.title, callback_data=f'my_anime_{anime.mal_id}')
            
            if current_page > 1:
                builder.button(text='Назад', callback_data=f'deafult_prev_{current_page - 1}_{total_pages}')
            
            if current_page < total_pages:
                builder.button(text='Вперед', callback_data=f'deafult_prev_{current_page + 1}_{total_pages}')

        await message.answer(f'Ваши аниме: {current_page}/{total_pages}', reply_markup=builder.adjust(2).as_markup())



async def deafult_shift(callback: CallbackQuery):

    current_page, total_pages = callback.data.split('_')[2:]
    current_page = int(current_page)
    total_pages = int(total_pages)

    new_offset = (current_page - 1) * 10

    async with Session() as session:
        current_animes = await session.scalars(select(Anime).offset(new_offset).limit(10))
        animes = current_animes.all()

        if animes:
            builder = InlineKeyboardBuilder()
            for anime in animes:
                builder.button(text=anime.title, callback_data=f'my_anime_{anime.mal_id}')
            
            if current_page > 1:
                builder.button(text='Назад', callback_data=f'deafult_prev_{current_page - 1}_{total_pages}')
            
            if current_page < total_pages:
                builder.button(text='Вперед', callback_data=f'deafult_next_{current_page + 1}_{total_pages}')
            

            await callback.message.edit_text(f'{current_page}/{total_pages}', reply_markup=builder.adjust(2).as_markup())