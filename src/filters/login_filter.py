from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import SimpleCustomFilter

from src.database.repo import get_user_by_telegram_id


class LoginFilter(SimpleCustomFilter):
    key = "check_login"

    def __init__(self, bot: AsyncTeleBot):
        self.bot = bot

    async def check(self, message):
        user = await get_user_by_telegram_id(message.from_user.id)

        if user is None:
            await self.bot.reply_to(
                message,
                "Вы не сохранены в системе. Пожалуйста, напишите команду /remember_me, чтобы добавить репозиторий.",
            )
            return False

        return True
