from aiogram import F,  Router
from aiogram.types import callback_query, CallbackQuery, Message, message, InputMediaPhoto
from sqlalchemy import func, select
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..database import Session, Anime, User, UserAnime
from ..utils import UserState
from ..keyboards import button_work_with_library

library_inline_handler = Router()



# anime_inline_buttons
@library_inline_handler.callback_query(F.data.startswith('planned_anime_mal_id:'))
async def get_planned_bunner_anime(callback: CallbackQuery):

    await callback.answer()
    mal_id = callback.data.split(':')[1]
    mal_id = int(mal_id)

    user_id = callback.from_user.id 

    async with Session() as session:
        await callback.message.delete()
        current_mal_id = await session.scalar(select(UserAnime.mal_id).filter(UserAnime.user_id == user_id, UserAnime.mal_id == mal_id))
        if current_mal_id:
            anime_bunner = await session.scalar(select(Anime).filter(Anime.mal_id == mal_id))
            if anime_bunner:
                await callback.message.answer_photo(photo=anime_bunner.photo_url,
                                                    caption=f'Title: {anime_bunner.title}\n\nSynopsis:{anime_bunner.synopsis[:200]}\n\nLast episode: {anime_bunner.last_episode}',
                                                    reply_markup=button_work_with_library(anime_mal_id=anime_bunner.mal_id))


#looked 
@library_inline_handler.callback_query(F.data.startswith('add_to_looked_anime_'))
async def change_status_looked(callback: CallbackQuery):

    await callback.answer()
    user_id = callback.from_user.id
    mal_id = callback.data.split('_')[4]

    async with Session.begin() as session:
        user_anime = await session.scalar(select(UserAnime).filter(UserAnime.user_id == user_id, UserAnime.mal_id == mal_id))
        if user_anime:
            user_anime.status = 'looked'
            await callback.message.delete()
            await callback.message.answer('Вы успешно изменили статус!')
        else:
            await callback.message.reply('Данное аниме не найдено')



# remove
@library_inline_handler.callback_query(F.data.startswith('remove_anime_'))
async def remove_anime(callback: CallbackQuery):

    await callback.answer()
    mal_id = callback.data.split('_')[2]
    user_id = callback.from_user.id

    async with Session.begin() as session:
        user_anime = await session.scalar(select(UserAnime).filter(UserAnime.user_id == user_id, UserAnime.mal_id == mal_id))
        if user_anime:
            await callback.message.delete()
            await session.delete(user_anime)
            await callback.message.answer('Аниме успешно удалено!')
        else:
            await callback.message.reply('Данное аниме не найдено')