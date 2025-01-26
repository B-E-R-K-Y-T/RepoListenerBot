from telebot.asyncio_filters import SimpleCustomFilter

from config import settings


class Admin:
    id = settings.ADMIN_ID


class AdminFilter(SimpleCustomFilter):
    """
    Filter for admin users
    """

    key = "check_admin"

    async def check(self, message):
        if settings.DEBUG:
            return True

        return int(message.from_user.id) == int(Admin.id)
