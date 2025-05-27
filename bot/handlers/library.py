from aiogram import F,  Router
from aiogram.types import callback_query, CallbackQuery, Message, message
from sqlalchemy import func, select

from ..database import Session, Anime, User, UserAnime

library_handler = Router()

@library_handler.callback_query(F.data.startswith('add_to_lib_'))
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


# @library_handler.message(F.text == '📚 My Library')
# async def get_list_library(message: Message):

#     user_id = message.from_user.id 
#     current_page = 1

#     async with Session() as session:
#         count = await session.scalar(select(func.count(UserAnime.id)).filter(UserAnime.user_id==user_id))
#         offset = (current_page - 1) * 1

#         current_anime = await session.scalar(select(UserAnime.anime).order_by(UserAnime.id).offset(offset).limit(1))

#         await message.answer(current_anime.title)
