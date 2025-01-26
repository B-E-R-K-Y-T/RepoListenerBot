from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class Uploader(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: str
    url: HttpUrl
    html_url: HttpUrl
    followers_url: HttpUrl
    following_url: HttpUrl
    gists_url: HttpUrl
    starred_url: HttpUrl
    subscriptions_url: HttpUrl
    organizations_url: HttpUrl
    repos_url: HttpUrl
    events_url: HttpUrl
    received_events_url: HttpUrl
    type: str
    site_admin: bool


class Asset(BaseModel):
    url: HttpUrl
    browser_download_url: HttpUrl
    id: int
    node_id: str
    name: str
    label: Optional[str] = None
    state: str
    content_type: str
    size: int
    download_count: int
    created_at: str
    updated_at: str
    uploader: Uploader


class Author(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: str
    url: HttpUrl
    html_url: HttpUrl
    followers_url: HttpUrl
    following_url: HttpUrl
    gists_url: HttpUrl
    starred_url: HttpUrl
    subscriptions_url: HttpUrl
    organizations_url: HttpUrl
    repos_url: HttpUrl
    events_url: HttpUrl
    received_events_url: HttpUrl
    type: str
    site_admin: bool


class Release(BaseModel):
    owner: str
    repo: str
    url: HttpUrl
    html_url: HttpUrl
    assets_url: HttpUrl
    upload_url: HttpUrl
    tarball_url: HttpUrl
    zipball_url: HttpUrl
    id: int
    node_id: str
    tag_name: str
    target_commitish: str
    name: str
    body: str
    draft: bool
    prerelease: bool
    created_at: str
    published_at: str
    author: Author
    assets: List[Asset]
