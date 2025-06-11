import asyncio
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select

from ..utils import UserState
from ..database import UserAnime, Session, Anime
from ..keyboards import anime_buttons_changed_btn_add_to_waching_or_not

library_reply_handler = Router()


async def get_anime_on_filter(message: Message, bot: Bot, filter: str, caption: str, other_text: str):

    user_id = message.from_user.id
    async with Session() as session:
        planned_anime = await session.scalars(select(UserAnime.mal_id).filter(UserAnime.user_id == user_id, UserAnime.status == filter))
        all_planned_mal_ids = planned_anime.all()

        if all_planned_mal_ids:
            await message.answer(f'Ваши {caption} аниме:')
            for m_id in all_planned_mal_ids:
                anime = await session.scalar(select(Anime).filter(Anime.mal_id == m_id))
                await bot.send_photo(
                    chat_id=user_id,
                    photo=anime.image,
                    caption=f'Title: {anime.title}\n\nSynopsis: {anime.synopsis[:500]}...More\n\nEpisodes: {anime.episodes}',
                    reply_markup=anime_buttons_changed_btn_add_to_waching_or_not(anime.mal_id, filter)
                )
                await asyncio.sleep(0.3) # pagination cooming soon...
        
        else:
            await message.answer(other_text)



@library_reply_handler.message(F.text == '📅 В планах', UserState.user_action)
async def get_planned_anime(message: Message, bot: Bot):

    caption = 'запланированные'
    filter = 'planned'
    other_text = 'У вас нет ниодного аниме для просмотра. Вы можете найти и добавить его в библиотеку'

    await get_anime_on_filter(message=message, bot=bot, filter=filter, caption=caption, other_text=other_text)



@library_reply_handler.message(F.text == '✅ Просмотренные')
async def get_viewed_anime(message: Message, bot: Bot):

    caption = 'просмотренные'
    filter = 'viewed'
    other_text = 'У вас нет ниодного просмотренного аниме.'

    await get_anime_on_filter(message=message, bot=bot, filter=filter, caption=caption, other_text=other_text)



@library_reply_handler.message(F.text == '🗑️ Удалить', UserState.user_action)
async def get_anime_for_deleted(message: Message):

    user_id = message.from_user.id

    async with Session() as session:
        scalars_anime = await session.scalars(select(UserAnime.mal_id).filter(UserAnime.user_id == user_id))
        mal_ids = scalars_anime.all()

        if not mal_ids:
            await message.answer('У вас нет аниме для удаления')
            return

        builder = InlineKeyboardBuilder()
        for mal_id in mal_ids:
            anime = await session.scalar(select(Anime).filter(Anime.mal_id == mal_id))
            if anime:
                builder.button(text=f'{anime.title}', callback_data=f'anime_for_deleted:{anime.mal_id}')
        await message.answer('Выберите аниме, которое хотите удалить из библиотеки:', reply_markup=builder.adjust(3).as_markup())



@library_reply_handler.callback_query(F.data.startswith('anime_for_deleted:'))
async def deleted_current_anime_for_library(callback: CallbackQuery):

    await callback.message.delete()
    mal_id = callback.data.split(':')[1]
    user_id = callback.from_user.id

    async with Session.begin() as session:

        user_anime = await session.scalar(select(UserAnime).filter(UserAnime.user_id == user_id, UserAnime.mal_id == mal_id))
        if user_anime:
            await session.delete(user_anime)
            await callback.message.answer('Аниме успешно удалено!')
