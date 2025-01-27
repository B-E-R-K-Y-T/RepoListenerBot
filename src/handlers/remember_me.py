from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.database.repo import get_user_by_telegram_id, add_user
from src.services.log import logger


async def remember_me_command_handler(message: Message, bot: AsyncTeleBot):
    logger.info(f"User {message.from_user.id} send request to remember him")

    user = await get_user_by_telegram_id(message.from_user.id)

    if user is not None:
        await bot.send_message(message.chat.id, "А я и так уже Вас знаю 🖕🏻")

        return

    await bot.send_message(message.chat.id, "Приятно познакомиться! 👋🏻")
    await add_user(message.from_user.id, True)
