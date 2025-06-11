from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from sqlalchemy import select


from ..database import UserAnime, Session, User, Anime
from ..keyboards import anime_interaction_buttons
from ..utils.anime_pagination import shift_index

anime_interaction_handler = Router()



@anime_interaction_handler.callback_query(F.data.startswith('back:to:pagination_'))
async def back_to_scroll_anime(callback: CallbackQuery, state: FSMContext):

    await shift_index(callback, state)



@anime_interaction_handler.callback_query(F.data.startswith('add_planned:'))
async def add_anime_in_planned(callback: CallbackQuery):

    await callback.answer()
    mal_id = callback.data.split(':')[1]
    user_id = callback.from_user.id 

    async with Session.begin() as session:

        user = await session.scalar(select(User).filter(User.id == user_id))
        anime = await session.scalar(select(Anime).filter(Anime.mal_id == mal_id))

        if user and anime:
            exiting = await session.scalar(select(UserAnime).filter(UserAnime.user_id == user.id, UserAnime.mal_id == anime.mal_id))
            if not exiting:
                session.add(UserAnime(
                    user_id = user.id,
                    anime_id = anime.id,
                    mal_id = mal_id,
                    ))
                await session.flush()
                await callback.message.answer('Аниме успешно добавлено в вашу библиотеку!')
            
            else:
                await callback.message.reply('Данное аниме уже находится у вас в библиотеке!')
        else:
            await callback.message.answer('Не удалось найти аниме или пользователя, возможно произошел сбой, попробуйте позднее')



@anime_interaction_handler.callback_query(F.data.startswith('trailer:'))
async def get_trailer_anime(callback: CallbackQuery):

    await callback.answer()
    mal_id = callback.data.split(':')[1]

    async with Session() as session:
        anime = await session.scalar(select(Anime).filter(Anime.mal_id == mal_id))
        if anime:
            trailer_url = anime.trailer
            if trailer_url != 'Нету':
                await callback.message.answer(f'Трейлер на аниме - {anime.title}\n{trailer_url}')
            else:
                await callback.message.answer('Нет трейлера на данное аниме.')
        else:
            await callback.message.answer('Аниме не найдено, произошел сбой. Попробуйте поздней')



@anime_interaction_handler.callback_query(F.data.startswith('description:'))
async def get_full_synopsis(callback: CallbackQuery):

    await callback.answer()
    mal_id = callback.data.split(':')[1]

    async with Session() as session:
        anime = await session.scalar(select(Anime).filter(Anime.mal_id == mal_id))
        if anime:
            await callback.message.answer(
                anime.synopsis,
                parse_mode='HTML'
            )



@anime_interaction_handler.callback_query(F.data.startswith('add_watching:'))
async def add_anime_to_wathcing(callback: CallbackQuery):

    await callback.answer()
    user_id = callback.from_user.id
    mal_id = callback.data.split(':')[1]

    async with Session.begin() as session:
        user_anime_status = await session.scalar(select(UserAnime).filter(UserAnime.user_id == user_id, UserAnime.mal_id == mal_id))
        if user_anime_status:
            user_anime_status.status = 'viewed'
            await callback.message.delete()
            await callback.message.answer('Вы успешно добавили в просмотренное')