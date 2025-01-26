from telebot.asyncio_handler_backends import State, StatesGroup


class RepoCreateState(StatesGroup):
    waiting_repo = State()
    waiting_owner = State()


class RepoDeleteState(StatesGroup):
    waiting_repo = State()
    waiting_owner = State()
