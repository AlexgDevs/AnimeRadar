from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def main_menu() -> ReplyKeyboardMarkup:
    '''Main menu'''

    builder = ReplyKeyboardBuilder()
    builder.button(text='🔍 Search Anime') #.
    builder.button(text='📚 My Library') #.
    builder.button(text='🏆 Top Anime') #.
    builder.button(text='🔔 Notifications')#. 
    
    return builder.adjust(2, 2, 2).as_markup(resize_keyboard=True)

def library_menu() -> ReplyKeyboardMarkup:
    '''Library menu'''

    builder = ReplyKeyboardBuilder()
    builder.button(text='👀 Watching')
    builder.button(text='✅ Completed')
    builder.button(text='📅 Planned')
    builder.button(text='🗑️ Remove')
    builder.button(text='🔙 Back to Main')

    return builder.adjust(2, 2, 1).as_markup(resize_keyboard=True)

def back_only() -> ReplyKeyboardMarkup:
    '''Back to main menu'''

    builder = ReplyKeyboardBuilder()
    builder.button(text='🔙 Back')

    return builder.as_markup(resize_keyboard=True)







