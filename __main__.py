import asyncio

from app import start


async def main():
    await start()


if __name__ == "__main__":
    asyncio.run(main())
