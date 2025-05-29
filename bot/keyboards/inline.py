from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def anime_inline_buttons(anime_mal_id: int) -> InlineKeyboardMarkup:
    '''Anime actions'''

    builder = InlineKeyboardBuilder()
    builder.button(text='➕ Add', callback_data=f"add_{anime_mal_id}")
    builder.button(text='🔔 Notify', callback_data=f"notify_{anime_mal_id}")
    builder.button(text='ℹ️ Info', callback_data=f"info_{anime_mal_id}")
    builder.button(text='🎬 Similar', callback_data=f"similar_{anime_mal_id}")
    
    return builder.adjust(2, 2).as_markup()

def button_work_with_library(anime_mal_id: int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.button(text='I looked at', callback_data=f'add_to_looked_anime_{anime_mal_id}') 
    builder.button(text='Additional Info', callback_data=f'see_more_anime_{anime_mal_id}')
    builder.button(text='Remove', callback_data=f'remove_anime_{anime_mal_id}')
    builder.button(text='Trailer', callback_data=f'get_trailer_anime_{anime_mal_id}')
    builder.button(text='Notifications', callback_data=f'get_notification_anime_{anime_mal_id}')

    return builder.adjust(2, 2, 1).as_markup()


# I looked at the additional information. Remove. Notifications. The trailer