from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.database.repo import get_user_by_telegram_id, update_user
from src.services.log import logger


async def off_notify_command_handler(message: Message, bot: AsyncTeleBot):
    logger.info(f"User {message.from_user.id} off notify")

    user = await get_user_by_telegram_id(message.from_user.id)

    if user is None:
        await bot.send_message(message.chat.id, "Пользователь не найден")

        return

    await update_user(user.telegram_id, False)
    await bot.send_message(message.chat.id, "Уведомления больше не будут приходить 😓")
