from telebot.async_telebot import AsyncTeleBot
from telebot.states.asyncio import StateContext
from telebot.types import Message

from src.services.log import logger


async def cancel_command_handler(message: Message, bot: AsyncTeleBot, state: StateContext):
    logger.info(f"User {message.from_user.first_name} send cancel command")

    await state.delete()
    await bot.send_message(message.chat.id, "Действие отменено.")
