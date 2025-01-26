import asyncio
from collections.abc import Callable
from functools import wraps

from src.schedule import stop_event
from src.services.log import logger


def task_runner(interval: float = 60):
    sleep_time = interval

    def task(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"Starting task '{func.__name__}'")
            result = None

            while not stop_event.is_set():
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in task '{func.__name__}': {e}")

                await asyncio.sleep(sleep_time)

            logger.info(f"Finishing task '{func.__name__}'")
            return result

        return wrapper

    return task
