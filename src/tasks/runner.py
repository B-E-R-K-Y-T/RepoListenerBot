import asyncio
from collections.abc import Callable
from functools import wraps

from src.schedule import stop_event
from src.services.log import logger


def task_runner(interval: float = 60, once: bool = False):
    sleep_time = interval

    def task(func: Callable):
        async def _once_call(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in task '{func.__name__}': {e}")

        async def _loop_call(*args, **kwargs):
            while not stop_event.is_set():
                _result = await _once_call(*args, **kwargs)
                await asyncio.sleep(sleep_time)

            return _result

        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"Starting task '{func.__name__}'")

            if once:
                result = await _once_call(*args, **kwargs)
            else:
                result = await _loop_call(*args, **kwargs)

            logger.info(f"Finishing task '{func.__name__}'")
            return result

        return wrapper

    return task
