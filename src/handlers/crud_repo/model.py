from typing import Optional


class Repo:
    def __init__(self, repo: Optional[str], owner: Optional[str]):
        self.repo = repo
        self.owner = owner
