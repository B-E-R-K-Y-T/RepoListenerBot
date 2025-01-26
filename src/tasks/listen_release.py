import asyncio

from config import settings
from src.database.repo import get_all_repos, get_user_repos, get_all_users
from src.models.release import Release
from src.integrations.rest import http_repository
from src.services.log import logger
from src.task_queues import NotificationEventRelease, notification_event_queue
from src.tasks.runner import task_runner


@task_runner(interval=settings.TASK_RELEASE_INTERVAL_CHECK)
async def release_listen():
    logger.info("Listing releases...")

    current_repos = await get_all_repos()
    tasks = []

    for repo in current_repos:
        tasks.append(http_repository.get_releases(repo.owner, repo.repo))

    repo_releases: list[list[Release]] = await asyncio.gather(*tasks)
    users = await get_all_users()

    for user in users:
        user_repos = await get_user_repos(user.telegram_id)

        for repo in repo_releases:
            if not repo:
                continue

            last_release = repo[0]

            for user_repo in user_repos:
                if (
                    last_release.owner == user_repo.owner
                    and
                    last_release.repo == user_repo.repo
                ):
                    if last_release.tag_name != user_repo.current_version:
                        logger.info(f"New release: {last_release.tag_name}")

                        user_repo.old_version = user_repo.current_version
                        user_repo.current_version = last_release.tag_name
                        await user_repo.save()

                        event = NotificationEventRelease(
                            telegram_id=user.telegram_id,
                            release=last_release,
                        )
                        await notification_event_queue.put(event)

            logger.info(f"Release tag: {last_release.tag_name}")
