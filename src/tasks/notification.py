import asyncio

from telebot.async_telebot import AsyncTeleBot

from config import settings
from src.services.log import logger
from src.task_queues import notification_event_queue, NotificationEventRelease
from src.tasks.runner import task_runner


@task_runner(interval=settings.NOTIFY_INTERVAL_CHECK)
async def notification_manager(bot: AsyncTeleBot):
    logger.info("Checking notify about new releases...")

    task_messages = []

    while not notification_event_queue.empty():
        notification_event: NotificationEventRelease = (
            notification_event_queue.get_nowait()
        )

        task_messages.append(
            bot.send_message(
                notification_event.telegram_id,
                f"У {notification_event.release.repo} новая версия! {notification_event.release.name}",
            )
        )

    if not task_messages:
        return

    logger.info("Sending notifications...")

    try:
        async with asyncio.TaskGroup() as tg:
            for task in task_messages:
                tg.create_task(task)
    except* Exception as e:
        logger.error(f"Error sending notification: {e}")
