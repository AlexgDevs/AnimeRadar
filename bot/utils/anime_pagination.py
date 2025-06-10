from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InputMediaPhoto

async def main_pagination(message, current_index, anime_list):

    count = len(anime_list)
    current_anime = anime_list[current_index]
    
    prev_next_builder = InlineKeyboardBuilder()

    if current_index < count - 1:
        prev_next_builder.button(text='Вперед', callback_data=f'next_{current_index + 1}_{count}')
    
    if current_index > 1:
        prev_next_builder.button(text='Назад', callback_data=f'prev_{current_index - 1}_{count}')

    await message.answer_photo(photo=current_anime['image'], caption=f'page {current_index + 1} is {count}', reply_markup=prev_next_builder.as_markup())


async def shift_index(callback, state):

    await callback.answer()
    data = await state.get_data()
    anime_list = data.get('anime_list')

    current_index, count = callback.data.split('_')[1:]

    current_index = int(current_index)
    count = int(count)

    current_anime = anime_list[current_index]

    prev_next_builder = InlineKeyboardBuilder()
    
    if current_index > 0:
        prev_next_builder.button(text='Назад', callback_data=f'prev_{current_index - 1}_{count}')

    if current_index < count - 1:
        prev_next_builder.button(text='Вперед', callback_data=f'next_{current_index + 1}_{count}')
    
    await callback.message.edit_media(media=InputMediaPhoto(media=current_anime['image'], caption=f'page {current_index + 1} is {count}'), reply_markup=prev_next_builder.as_markup())

