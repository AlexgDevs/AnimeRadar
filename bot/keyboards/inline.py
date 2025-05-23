from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def anime_inline_buttons(anime_id: int) -> InlineKeyboardMarkup:
    '''Anime actions'''

    builder = InlineKeyboardBuilder()
    builder.button(text='➕ Add', callback_data=f"add_{anime_id}")
    builder.button(text='🔔 Notify', callback_data=f"notify_{anime_id}")
    builder.button(text='ℹ️ Info', callback_data=f"info_{anime_id}")
    builder.button(text='🎬 Similar', callback_data=f"similar_{anime_id}")
    
    return builder.adjust(2, 2).as_markup()