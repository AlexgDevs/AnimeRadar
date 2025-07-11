from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy import func, select

from ..API.parse_anime import search_anime
from ..database import Anime, Session
from ..utils import UserState, QueryAnime, shift_index, index_pagination, deafult_pagination, deafult_shift
from ..keyboards import (

    main_menu,
    library_menu,
    stop_search_button,
    anime_interaction_buttons

)


config_handler = Router()


@config_handler.message(F.text.in_(['📚 Моя библиотека', '🔙 Назад']), UserState.user_action)
async def keyboard_to_change_library_menu(message: Message):

    if message.text == '📚 Моя библиотека':
        await message.answer('Вы вошли в меню библиотеки', reply_markup=library_menu())

    if message.text == '🔙 Назад':
        await message.answer('Вы вернулись в главное меню', reply_markup=main_menu())



@config_handler.message(F.text == 'Стоп', QueryAnime.await_anime_query)
async def stopped_search_anime(message: Message, state: FSMContext):

    await message.answer('Прекращен поиск аниме', reply_markup=main_menu())
    await state.clear()
    await state.set_state(UserState.user_action)



@config_handler.message(F.text == '🔍 Поиск аниме', UserState.user_action)
async def request_title(message: Message, state: FSMContext):

    await message.answer('Введите название аниме', reply_markup=stop_search_button())
    await state.set_state(QueryAnime.await_anime_query)



@config_handler.message(F.text, QueryAnime.await_anime_query)
async def get_json_current_anime_with_title(message: Message, state: FSMContext):

    title = message.text

    anime_list = await search_anime(title, False)
    if anime_list is not None:
        
        await state.update_data(anime_list=anime_list)
        async with Session.begin() as session:
            
            anime_mal_ids = set(await session.scalars(select(Anime.mal_id)))
            anime_for_adding = []

            for anime_dict in anime_list:
                if anime_dict['mal_id'] not in anime_mal_ids:
                    anime_for_adding.append(Anime(**anime_dict))
            
            if anime_for_adding:
                session.add_all(anime_for_adding)
                await session.flush()
    
        await index_pagination(message=message, current_index=0, anime_list=anime_list)

    else:
        await message.answer('Такого аниме нет, попробуй еще раз')



@config_handler.callback_query(F.data.startswith('mal_id_current_anime:'))
async def get_buttons_iteractions_for_anime(callback: CallbackQuery):

    await callback.answer()
    mal_id, count, current_index = callback.data.split(':')[1:]
    count = int(count)
    current_index = int(current_index)

    async with Session() as session:
        current_anime = await session.scalar(select(Anime).filter(Anime.mal_id == mal_id))
        if current_anime:
            await callback.message.edit_media(
                media=InputMediaPhoto(
                media=current_anime.image,
                caption=f'Episodes: {current_anime.episodes}'),
                reply_markup=anime_interaction_buttons(mal_id=current_anime.mal_id, count=count, current_index=current_index))


@config_handler.callback_query(F.data.startswith(('next_', 'prev_')))
async def handle_pagination(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await shift_index(callback, state)



@config_handler.message(F.text == 'Последнее добавленные аниме', UserState.user_action)
async def get_last_anime_list(message: Message):

    await deafult_pagination(message=message, current_page=1)


@config_handler.callback_query(F.data.startswith(('deafult_prev_', 'deafult_next_')))
async def get_deafult_shift(callback: CallbackQuery):

    await deafult_shift(callback=callback)
