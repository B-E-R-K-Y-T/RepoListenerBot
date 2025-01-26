from asyncio import Queue

from typing_extensions import NamedTuple

from src.models.release import Release


class NotificationEventRelease(NamedTuple):
    telegram_id: int
    release: Release


notification_event_queue = Queue(maxsize=5)
