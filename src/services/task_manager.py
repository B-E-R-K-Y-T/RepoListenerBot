import asyncio
from asyncio import Task

from config import settings
from src.services.log import logger


class TaskManager:
    def __init__(self, tasks: tuple, timeout: float = settings.TIME_TASKS_WAIT):
        self.unstarted_tasks = tasks
        self.active_tasks = []
        self.timeout = timeout

    def start(self):
        for task in self.unstarted_tasks:
            self.active_tasks.append(asyncio.create_task(task))

    async def _task_waiter(self, task: Task):
        try:
            await asyncio.wait_for(task, timeout=self.timeout)
        except asyncio.TimeoutError:
            logger.warning(f"Task '{task}' timeout")
        except Exception as e:
            logger.error(f"Task '{task}' error: {e}")
        else:
            logger.info(f"Task '{task}' finished")

    async def wait_for_tasks(self):
        logger.info(
            f"Start waiting for {len(self.active_tasks)} tasks... Timeout: {self.timeout} sec."
        )

        async with asyncio.TaskGroup() as tg:
            for task in self.active_tasks:
                tg.create_task(self._task_waiter(task))

        logger.info("All tasks finished")
