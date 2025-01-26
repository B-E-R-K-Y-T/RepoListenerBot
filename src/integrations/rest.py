import aiohttp

from config import settings
from src.models.release import Release
from src.services.log import logger


class HttpRepository:
    def __init__(self):
        self.session = None
        self.headers = {
            "Authorization": f"token {settings.GITHUB_API_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def set_session(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_releases(self, owner: str, repo: str) -> list[Release]:
        url = "https://api.github.com/repos/{owner}/{repo}/releases".format(
            owner=owner, repo=repo
        )

        async with self.session.get(url, headers=self.headers) as response:
            if response.ok:
                response_json = await response.json()

                for release in response_json:
                    release["repo"] = repo
                    release["owner"] = owner

                logger.info(f"Successfully retrieved releases for {owner}/{repo}")
                return [Release(**release) for release in response_json]
            else:
                logger.error(f"Error: {response.status}, url: {url}")
                return []

    async def close(self):
        await self.session.close()


http_repository = HttpRepository()
