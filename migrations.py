import asyncio
from tortoise import Tortoise

from src.database.models import User, Repo  # noqa
from config import settings


async def create_tables():
    """Создание таблиц users и repos, если они не существуют."""
    await Tortoise.init(
        db_url=f"sqlite://{settings.DATABASE_NAME}",
        modules={"models": ["src.database.models"]},
    )
    await Tortoise.generate_schemas()


# Пример использования класса
async def main():
    await create_tables()
    print("Миграция завершена! ✨💫🎂🍰🎉")
    await Tortoise.close_connections()  # Закрытие соединений с базой данных


# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(main())
