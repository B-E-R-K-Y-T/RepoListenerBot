import asyncio

import aiohttp
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter
from telebot.asyncio_storage import StateMemoryStorage
from telebot.states.asyncio import StateMiddleware

from config import settings
from src.handlers.cancel import cancel_command_handler
from src.handlers.crud_repo.delete_repo import delete_repo_command_handler, get_delete_repo_name, get_delete_owner_name
from src.schedule import stop_app_lock, stop_event
from src.database.repo import close_db, init_db
from src.filters.admin_filter import AdminFilter
from src.filters.login_filter import LoginFilter
from src.handlers.crud_repo.add_repo import add_repo_command_handler, get_repo_name, get_owner_name
from src.handlers.core import Handler, Ignore
from src.handlers.off_notify import off_notify_command_handler
from src.handlers.on_notify import on_notify_command_handler
from src.handlers.remember_me import remember_me_command_handler
from src.handlers.crud_repo.show_repos import show_repos_command_handler
from src.handlers.start import start_command_handler
from src.handlers.states.repos import RepoCreateState, RepoDeleteState
from src.integrations.rest import http_client
from src.middlewares.antiflood import AntiFloodMiddleware
from src.services.log import logger
from src.services.task_manager import TaskManager
from src.tasks.listen_release import release_listen
from src.tasks.notification import notification_manager

bot = AsyncTeleBot(
    token=settings.TELEGRAM_API_TOKEN,
    state_storage=StateMemoryStorage(),
)


HANDLERS = (
    Handler(callback=start_command_handler, commands=["start"], pass_bot=True),
    Handler(callback=off_notify_command_handler, commands=["off_notify", "off_n"], pass_bot=True),
    Handler(callback=on_notify_command_handler, commands=["on_notify", "on_n"], pass_bot=True),
    Handler(callback=show_repos_command_handler, commands=["show_repos", "sr"], pass_bot=True),
    Handler(callback=add_repo_command_handler, commands=["add_repo", "ar"], pass_bot=True),
    Handler(callback=delete_repo_command_handler, commands=["delete_repo", "dr"], pass_bot=True),
    Handler(callback=cancel_command_handler, commands=["cancel", "rollback"], pass_bot=True),
    Handler(callback=remember_me_command_handler, commands=["remember_me", "rm"], pass_bot=True, check_login=Ignore()),
    Handler(callback=get_repo_name, pass_bot=True, state=RepoCreateState.waiting_repo),
    Handler(callback=get_owner_name, pass_bot=True, state=RepoCreateState.waiting_owner),
    Handler(callback=get_delete_repo_name, pass_bot=True, state=RepoDeleteState.waiting_repo),
    Handler(callback=get_delete_owner_name, pass_bot=True, state=RepoDeleteState.waiting_owner),
)
TASKS = (
    release_listen(),
    notification_manager(bot),
)
FILTERS = (
    AdminFilter(),
    StateFilter(bot),
    LoginFilter(bot),
)
MIDDLEWARES = (
    AntiFloodMiddleware(
        time_limit=settings.INTERVAL_LIMIT_MESSAGES,
        message_limit=settings.LIMIT_MESSAGES,
        bot=bot
    ),
    StateMiddleware(bot)
)

task_manager = TaskManager(TASKS)


def init_filters():
    for filter_ in FILTERS:
        bot.add_custom_filter(filter_)


def init_handlers():
    def register(callback, commands, pass_bot=False, check_admin=True, state=None, **kwargs):
        new_kwargs = {}

        for k, v in kwargs.items():
            if isinstance(v, Ignore):
                continue

            new_kwargs[k] = v

        bot.register_message_handler(
            callback=callback,
            commands=commands,
            pass_bot=pass_bot,
            check_admin=check_admin,
            state=state,
            **new_kwargs
        )

    for handler in HANDLERS:
        register(
            callback=handler.callback,
            commands=handler.commands,
            pass_bot=handler.pass_bot,
            check_admin=handler.check_admin,
            state=handler.state,
            check_login=handler.check_login,
        )


def init_http():
    http_client.set_session(aiohttp.ClientSession())


def init_tasks():
    task_manager.start()


async def wait_for_tasks():
    await task_manager.wait_for_tasks()


def init_middlewares():
    for middleware in MIDDLEWARES:
        bot.setup_middleware(middleware)


async def bot_task():
    await bot.polling(non_stop=True)


async def start():
    if settings.DEBUG:
        logger.warning("-" * 100)
        logger.warning(" " * 30 + "Debug mode enabled. ADMIN FILTER OFF!")
        logger.warning("-" * 100)
        # Сделал так, чтобы можно было успеть прочитать
        await asyncio.sleep(1)

    init_handlers()
    init_filters()
    init_middlewares()
    init_http()
    init_tasks()
    await init_db()

    logger.info("Bot started.")
    await bot_task()
    logger.info("Bot stopped.")

    async with stop_app_lock:
        stop_event.set()

    logger.info("App stopping...")
    await wait_for_tasks()
    await http_client.close()
    await close_db()
    logger.info("App stopped.")
