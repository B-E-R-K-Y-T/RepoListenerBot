from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.database.repo import get_user_by_telegram_id
from src.services.log import logger


async def show_repos_command_handler(message: Message, bot: AsyncTeleBot):
    logger.info(f"User {message.from_user.id} send show_repos command")
    user = await get_user_by_telegram_id(message.from_user.id)

    if user is None:
        await bot.send_message(message.chat.id, "Вы не зарегистрированы.")

    repos = await user.get_repos()

    if not repos:
        await bot.send_message(message.chat.id, "У вас нет репозиториев 😭")

        return

    formated_repos = "\n".join(
        f"\n{i + 1}-й:\n\trepo: '{repo.repo}', \n\towner: '{repo.owner}', \n\trelease: '{repo.current_version}'"
        for i, repo in enumerate(repos)
    )

    await bot.send_message(message.chat.id, f"Репозитории:\n\n{formated_repos}")
