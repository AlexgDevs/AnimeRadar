from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):

    user_action = State()

class QueryAnime(StatesGroup):

    await_anime_query = State()