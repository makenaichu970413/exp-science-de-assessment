# Library
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl

# Utils
from utils.model.Igithub_issues import IGitHubReactions
from utils.model.Igithub_users import IGitHubUser


class IGitHubApp(BaseModel):
    id: Optional[int] = None
    client_id: Optional[str] = None
    slug: Optional[str] = None
    node_id: Optional[str] = None
    owner: Optional[IGitHubUser] = None
    name: Optional[str] = None
    description: Optional[str] = None
    external_url: Optional[HttpUrl] = None
    html_url: Optional[HttpUrl] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    permissions: Optional[dict] = None
    events: Optional[list[str]] = None


class IGitHubComment(BaseModel):
    url: Optional[HttpUrl] = None
    html_url: Optional[HttpUrl] = None
    issue_url: Optional[HttpUrl] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    user: Optional[IGitHubUser] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    author_association: Optional[str] = None
    body: Optional[str] = None
    reactions: Optional[IGitHubReactions] = None
    performed_via_github_app: Optional[IGitHubApp] = None
