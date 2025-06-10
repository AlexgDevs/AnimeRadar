from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InputMediaPhoto

async def main_pagination(message, current_index, anime_list):

    count = len(anime_list)
    current_anime = anime_list[current_index]
    
    prev_next_builder = InlineKeyboardBuilder()
    total_button = 0

    if current_index < count - 1:
        prev_next_builder.button(text='⭢', callback_data=f'next_{current_index + 1}_{count}')
        total_button += 1
    
    if current_index > 1:
        prev_next_builder.button(text='⭠', callback_data=f'prev_{current_index - 1}_{count}')
        total_button += 1

    prev_next_builder.button(text='Подробней', callback_data=f'mal_id_current_anime:{current_anime['mal_id']}:{count}:{current_index}')
    if total_button == 2:
        scroll_menu = prev_next_builder.adjust(2, 1).as_markup()
    else:
        scroll_menu = prev_next_builder.adjust(1, 1).as_markup()

    await message.answer_photo(photo=current_anime['image'], caption=f'page {current_index + 1} is {count}', reply_markup=scroll_menu)


async def shift_index(callback, state):

    await callback.answer()
    data = await state.get_data()
    anime_list = data.get('anime_list')

    current_index, count = callback.data.split('_')[1:]

    current_index = int(current_index)
    count = int(count)

    current_anime = anime_list[current_index]

    prev_next_builder = InlineKeyboardBuilder()
    total_button = 0

    if current_index > 0:
        prev_next_builder.button(text='⭠', callback_data=f'prev_{current_index - 1}_{count}')
        total_button += 1

    if current_index < count - 1:
        prev_next_builder.button(text='⭢', callback_data=f'next_{current_index + 1}_{count}')
        total_button += 1
        
    prev_next_builder.button(text='Подробней', callback_data=f'mal_id_current_anime:{current_anime['mal_id']}:{count}:{current_index}')
    if total_button == 2:
        scroll_menu = prev_next_builder.adjust(2, 1).as_markup()
    else:
        scroll_menu = prev_next_builder.adjust(1, 1).as_markup()

    await callback.message.edit_media(media=InputMediaPhoto(media=current_anime['image'], caption=f'page {current_index + 1} is {count}'), reply_markup=scroll_menu)

