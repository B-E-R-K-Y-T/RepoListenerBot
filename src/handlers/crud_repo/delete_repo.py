from telebot.async_telebot import AsyncTeleBot
from telebot.states.asyncio import StateContext
from telebot.types import Message

from src.database.repo import delete_repo, get_user_repos
from src.handlers.crud_repo.model import Repo
from src.handlers.states.repos import RepoDeleteState
from src.services.log import logger

repos: dict[int, Repo] = {}


async def delete_repo_command_handler(
    message: Message, bot: AsyncTeleBot, state: StateContext
):
    logger.info(f"User {message.from_user.id} is trying to delete repo")
    await bot.reply_to(message, "Пожалуйста, введите название репозитория:")
    repos[message.from_user.id] = Repo(repo=None, owner=None)

    await state.set(RepoDeleteState.waiting_repo)


async def get_delete_repo_name(
    message: Message, bot: AsyncTeleBot, state: StateContext
):
    logger.info(f"User {message.from_user.id} send name repo")
    repo_name = message.text
    target_repo = repos[message.from_user.id]
    target_repo.repo = repo_name

    await bot.reply_to(
        message,
        f"Вы указали репозиторий: '{repo_name}'. Пожалуйста, введите имя владельца репозитория:",
    )
    await state.set(RepoDeleteState.waiting_owner)


async def get_delete_owner_name(
    message: Message, bot: AsyncTeleBot, state: StateContext
):
    logger.info(f"User {message.from_user.id} send owner name")
    owner_name = message.text
    telegram_id = message.from_user.id

    target_repo = repos[telegram_id]
    target_repo.owner = owner_name

    user_repos = await get_user_repos(telegram_id)
    user_repos = [
        r
        for r in user_repos
        if r.repo == target_repo.repo and r.owner == target_repo.owner
    ]

    for user_repo in user_repos:
        await delete_repo(user_repo.id)

    if user_repos:
        await bot.send_message(
            message.chat.id, f"Репозиторий '{target_repo.repo}' удален"
        )
    else:
        await bot.send_message(
            message.chat.id, f"Репозиторий '{target_repo.repo}' не найден"
        )

    await state.delete()
    del repos[telegram_id]
    logger.info(f"User {message.from_user.id} delete repo")
