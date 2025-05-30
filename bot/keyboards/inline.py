from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def anime_inline_buttons(anime_mal_id: int, current_index: int, count: int) -> InlineKeyboardMarkup:
    '''Anime actions main_config.py'''

    builder = InlineKeyboardBuilder()
    builder.button(text='➕ Добавить', callback_data=f"add_to_library_{anime_mal_id}") # passed
    builder.button(text='ℹ️ Подробнее', callback_data=f"see_more_anime_{anime_mal_id}")
    builder.button(text='🎬 Трейлер', callback_data=f"trailer_anime_{anime_mal_id}")
    builder.button(text='🔙 Назад', callback_data=f"back_anime_{anime_mal_id}_{current_index}_{count}") # passed
    
    return builder.adjust(2, 2).as_markup()

def button_work_with_library(anime_mal_id: int) -> InlineKeyboardMarkup:
    '''Anime library actions library_inline_handler.py'''

    builder = InlineKeyboardBuilder()
    builder.button(text='👀 Я посмотрел(а)', callback_data=f'add_to_looked_anime_{anime_mal_id}') # passed 
    builder.button(text='ℹ️ Подробнее', callback_data=f'see_more_anime_{anime_mal_id}')
    builder.button(text='❌ Удалить', callback_data=f'remove_anime_{anime_mal_id}')
    builder.button(text='🎬 Трейлер', callback_data=f'trailer_anime_{anime_mal_id}')
    builder.button(text='🔔 Уведомление', callback_data=f'notification_anime_{anime_mal_id}')

    return builder.adjust(2, 2, 1).as_markup()


# I looked at the additional information. Remove. Notifications. The trailer