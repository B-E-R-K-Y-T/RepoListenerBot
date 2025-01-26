from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.states.asyncio import StateContext
from telebot.types import Message

from src.database.repo import get_user_by_telegram_id, add_repo
from src.handlers.crud_repo.model import Repo
from src.handlers.states.repos import RepoCreateState

repos: dict[int, Repo] = {}


async def add_repo_command_handler(
    message: Message, bot: AsyncTeleBot, state: StateContext
):
    await bot.reply_to(message, "Пожалуйста, введите название репозитория:")
    repos[message.from_user.id] = Repo(repo=None, owner=None)

    await state.set(RepoCreateState.waiting_repo)


async def get_repo_name(message: Message, bot: AsyncTeleBot, state: StateContext):
    repo_name = message.text
    repo = repos[message.from_user.id]
    repo.repo = repo_name

    await bot.reply_to(
        message,
        f"Вы указали репозиторий: '{repo_name}'. Пожалуйста, введите имя владельца репозитория:",
    )
    await state.set(RepoCreateState.waiting_owner)


async def get_owner_name(message: Message, bot: AsyncTeleBot, state: StateContext):
    owner_name = message.text
    repo = repos[message.from_user.id]
    repo.owner = owner_name

    await add_repo(
        repo.repo, repo.owner, user=await get_user_by_telegram_id(message.from_user.id)
    )
    await bot.reply_to(
        message,
        f"Репозиторий '{repo.repo}' принадлежит владельцу '{repo.owner}'. Данные сохранены.",
    )
    await state.delete()

    del repos[message.from_user.id]
