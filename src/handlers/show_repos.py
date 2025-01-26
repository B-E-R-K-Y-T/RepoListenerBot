from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.database.repo import get_all_repos


async def show_repos_command_handler(message: Message, bot: AsyncTeleBot):
    repos = await get_all_repos()

    if not repos:
        await bot.send_message(message.chat.id, "У вас нет репозиториев 😭")

        return

    formated_repos = "\n".join(
        f"{i + 1}-й: repo: '{repo.repo}', owner: '{repo.owner}'"
        for i, repo in enumerate(repos)
    )

    await bot.send_message(message.chat.id, f"Репозитории:\n\n{formated_repos}")
