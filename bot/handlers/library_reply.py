import asyncio
from aiogram import F, Router, Bot
from aiogram.types import Message
from sqlalchemy import select

from ..utils import UserState
from ..database import UserAnime, Session, Anime

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
                    caption=f'Title: {anime.title}\n\nSynopsis: {anime.synopsis[:500]}...More\n\nEpisodes: {anime.episodes}'
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



    # builder = ReplyKeyboardBuilder()
    # builder.button(text='✅ Просмотренные')
    # builder.button(text='📅 В планах')
    # builder.button(text='🗑️ Удалить')
    # builder.button(text='🔙 Назад')