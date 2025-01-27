import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.states.asyncio import StateContext
from telebot.types import Message

from src.database.repo import get_user_by_telegram_id, add_repo, repo_exists
from src.handlers.crud_repo.model import Repo
from src.handlers.states.repos import RepoCreateState
from src.integrations.rest import http_client
from src.models.release import Release
from src.services.log import logger

repos: dict[int, Repo] = {}


async def add_repo_command_handler(
    message: Message, bot: AsyncTeleBot, state: StateContext
):
    logger.info(f"User {message.from_user.id} added repo")
    await bot.reply_to(message, "Пожалуйста, введите название репозитория:")
    repos[message.from_user.id] = Repo(repo=None, owner=None)

    await state.set(RepoCreateState.waiting_repo)


async def get_repo_name(message: Message, bot: AsyncTeleBot, state: StateContext):
    logger.info(f"User {message.from_user.id} send name repo")
    repo_name = message.text
    repo = repos[message.from_user.id]
    repo.repo = repo_name

    await bot.reply_to(
        message,
        f"Вы указали репозиторий: '{repo_name}'. Пожалуйста, введите имя владельца репозитория:",
    )
    await state.set(RepoCreateState.waiting_owner)


async def get_owner_name(message: Message, bot: AsyncTeleBot, state: StateContext):
    logger.info(f"User {message.from_user.id} send name owner")
    owner_name = message.text
    repo = repos[message.from_user.id]
    repo.owner = owner_name

    try:
        await _process_repo(repo, message, bot)
    except* Exception as e:
        await bot.reply_to(message, f"Что-то пошло не так: {e}")
    finally:
        await state.delete()
        del repos[message.from_user.id]


async def _process_repo(repo: Repo, message: Message, bot: AsyncTeleBot):
    if await repo_exists(repo.repo, repo.owner):
        logger.info(f"Repo {repo.repo} already exists")
        await bot.reply_to(message, f"Репозиторий '{repo.repo}' уже существует 🖕🏻")

        return

    releases = await http_client.get_releases(repo.owner, repo.repo)

    if releases:
        await _save_repo(repo, message, bot, releases)
        logger.info(f"Repo {repo.repo} saved")

        return

    logger.info(f"Repo {repo.repo} not found")
    await bot.send_message(
        message.from_user.id,
        f"Репозиторий '{repo.repo}' не найден",
    )


async def _save_repo(repo: Repo, message: Message, bot: AsyncTeleBot, releases: list[Release]):
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
            add_repo(
                repo.repo,
                repo.owner,
                user=await get_user_by_telegram_id(message.from_user.id),
                current_version=releases[0].name
            )
        )
        tg.create_task(
            bot.send_message(
                message.from_user.id,
                f"Репозиторий '{repo.repo}' принадлежит владельцу '{repo.owner}'.\n\n"
                f"Последний релиз: '{releases[0].name}' сохранен.",
            )
        )
