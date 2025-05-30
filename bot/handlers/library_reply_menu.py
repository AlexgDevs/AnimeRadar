from aiogram import F,  Router
from aiogram.types import callback_query, CallbackQuery, Message, message, InputMediaPhoto
from sqlalchemy import func, select
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..database import Session, Anime, User, UserAnime
from ..utils import UserState
from ..keyboards import button_work_with_library

library_reply_handler = Router()




@library_reply_handler.message(F.text=='📅 Planned', UserState.user_action)
async def get_anime_for_watching(message: Message):

    user_id = message.from_user.id 

    async with Session() as session:
        planned_anime = await session.scalars(select(UserAnime.mal_id).filter(UserAnime.user_id == user_id, UserAnime.status == 'planned'))
        planned_anime_list = planned_anime.all()

        if not planned_anime_list:
            await message.answer('Anime not Found!')
            return
        
        builder = InlineKeyboardBuilder()
        for planned_anime in planned_anime_list:
            anime = await session.scalar(select(Anime).filter(Anime.mal_id == planned_anime))
            builder.button(text=f'{anime.title}', callback_data=f'planned_anime_mal_id:{anime.mal_id}')
    await message.answer('your_anime' , reply_markup=builder.adjust(2).as_markup())










# 