from telebot.async_telebot import AsyncTeleBot
from telebot.states.asyncio import StateContext
from telebot.types import Message


async def cancel_command_handler(message: Message, bot: AsyncTeleBot, state: StateContext):
    await state.delete()
    await bot.send_message(message.chat.id, "Действие отменено.")
