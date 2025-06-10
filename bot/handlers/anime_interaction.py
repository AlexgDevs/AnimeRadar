from aiogram import F, Router
from aiogram.types import callback_query, CallbackQuery
from aiogram.fsm.context import FSMContext
from ..keyboards import anime_interaction_buttons
from ..utils.anime_pagination import shift_index

anime_interaction_handler = Router()

@anime_interaction_handler.callback_query(F.data.startswith('back:to:pagination_'))
async def back_to_scroll_anime(callback: CallbackQuery, state: FSMContext):

    await shift_index(callback, state)