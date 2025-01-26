from typing import List

from tortoise import Model, fields


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    is_notified = fields.BooleanField()

    async def get_repos(self) -> List["Repo"]:
        return await Repo.filter(user=self).all()


class AuthUser(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    is_accessed = fields.BooleanField(default=False)
    user = fields.ForeignKeyField(
        "models.User", related_name="auth_users", on_delete=fields.CASCADE
    )


class Repo(Model):
    id = fields.IntField(pk=True)
    repo = fields.CharField(max_length=255)
    owner = fields.CharField(max_length=255)
    old_version = fields.CharField(max_length=50, null=True)
    current_version = fields.CharField(max_length=50, null=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="repos", on_delete=fields.CASCADE
    )
