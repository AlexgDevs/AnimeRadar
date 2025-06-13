from aiogram.utils.keyboard import InlineKeyboardBuilder

def anime_interaction_buttons(mal_id: int, count: int, current_index: int) -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()

    builder.button(text='📝 Добавить в планируемые', callback_data=f'add_planned:{mal_id}')
    builder.button(text='🎬 Трейлер', callback_data=f'trailer:{mal_id}')
    builder.button(text='📖 Полное описание', callback_data=f'description:{mal_id}')
    builder.button(text='🔙 Вернуться', callback_data=f'back:to:pagination_{current_index}_{count}')

    return builder.adjust(2, 1, 1).as_markup()


def anime_buttons_changed_btn_add_to_waching_or_not(mal_id: int, filter: str) -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()
    
    if filter == 'planned':
        builder.button(text='📺 Добавить в просмотренные', callback_data=f'add_watching:{mal_id}')
    
    builder.button(text='🎬 Трейлер', callback_data=f'trailer:{mal_id}')
    builder.button(text='📖 Полное описание', callback_data=f'description:{mal_id}')

    return builder.adjust(2, 1, 1).as_markup()


