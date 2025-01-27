from typing import Optional, List
from tortoise import Tortoise

from config import settings
from src.database.models import User, Repo


async def init_db() -> None:
    await Tortoise.init(
        db_url=f"sqlite://{settings.DATABASE_NAME}",
        modules={"models": ["src.database.models"]},
    )
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()


async def add_user(telegram_id: int, is_notified: bool) -> None:
    await User.create(telegram_id=telegram_id, is_notified=is_notified)


async def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    return await User.filter(telegram_id=telegram_id).first()


async def user_exists(telegram_id: int) -> bool:
    return await User.filter(telegram_id=telegram_id).exists()


async def get_all_users() -> List[User]:
    return await User.all()


async def update_user(telegram_id: int, is_notified: Optional[bool] = None) -> None:
    user = await User.filter(telegram_id=telegram_id).first()

    if user:
        if is_notified is not None:
            user.is_notified = is_notified
            await user.save()


async def delete_user(telegram_id: int) -> None:
    user = await User.filter(telegram_id=telegram_id).first()

    if user:
        await user.delete()

async def get_repo_by_id(repo_id: int) -> Optional[Repo]:
    return await Repo.filter(id=repo_id).first()


async def repo_exists_by_id(repo_id: int) -> bool:
    return await Repo.filter(id=repo_id).exists()


async def repo_exists(repo: str, owner: str) -> bool:
    return await Repo.filter(repo=repo, owner=owner).exists()


async def get_repo_by_name(repo: str, owner: str) -> Optional[Repo]:
    return await Repo.filter(repo=repo, owner=owner).first()


async def add_repo(
    repo: str,
    owner: str,
    user: User,
    old_version: Optional[str] = None,
    current_version: Optional[str] = None,
) -> None:
    await Repo.create(
        repo=repo,
        owner=owner,
        old_version=old_version,
        current_version=current_version,
        user=user,
    )


async def get_all_repos() -> List[Repo]:
    return await Repo.all()


async def update_repo(
    repo_id: int,
    repo: Optional[str] = None,
    owner: Optional[str] = None,
    old_version: Optional[str] = None,
    current_version: Optional[str] = None,
) -> None:
    repo_entity = await Repo.filter(id=repo_id).first()

    if repo_entity:
        if repo is not None:
            repo_entity.repo = repo
        if owner is not None:
            repo_entity.owner = owner
        if old_version is not None:
            repo_entity.old_version = old_version
        if current_version is not None:
            repo_entity.current_version = current_version
        await repo_entity.save()


async def delete_repo(repo_id: int) -> None:
    repo_entity = await Repo.filter(id=repo_id).first()

    if repo_entity:
        await repo_entity.delete()


async def get_user_repos(telegram_id: int) -> List[Repo]:
    user = await get_user_by_telegram_id(telegram_id)
    if user:
        return await user.get_repos()
    return []
