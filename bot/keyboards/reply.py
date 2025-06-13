from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def main_menu() -> ReplyKeyboardMarkup:
    '''Main menu'''

    builder = ReplyKeyboardBuilder()
    builder.button(text='🔍 Поиск аниме')
    builder.button(text='📚 Моя библиотека')
    builder.button(text='🏆 Топ 10 аниме по рейтингам')
    builder.button(text='🔔 Уведомления')
    builder.button(text='Последнее добавленные аниме')
    
    return builder.adjust(2, 2, 2).as_markup(resize_keyboard=True)



def library_menu() -> ReplyKeyboardMarkup:
    '''Library menu'''

    builder = ReplyKeyboardBuilder()
    builder.button(text='✅ Просмотренные')
    builder.button(text='📅 В планах')
    builder.button(text='🗑️ Удалить')
    builder.button(text='🔙 Назад')

    return builder.adjust(2, 2, 1).as_markup(resize_keyboard=True)



def stop_search_button() -> ReplyKeyboardMarkup:

    builder = ReplyKeyboardBuilder()
    builder.button(text='Стоп')
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)






