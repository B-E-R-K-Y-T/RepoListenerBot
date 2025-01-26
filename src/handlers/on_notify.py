from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from src.database.repo import get_user_by_telegram_id, update_user, add_user


async def on_notify_command_handler(message: Message, bot: AsyncTeleBot):
    user = await get_user_by_telegram_id(message.from_user.id)

    if user is None:
        await add_user(message.from_user.id, True)
    else:
        await update_user(user.telegram_id, True)

    await bot.send_message(message.chat.id, "Подписка на уведомления активирована! ✨")
