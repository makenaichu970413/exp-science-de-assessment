# Library
from pydantic import BaseModel
from typing import Optional


class IGitHubUser(BaseModel):
    login: Optional[str] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    avatar_url: Optional[str] = None
    gravatar_id: Optional[str] = None
    url: Optional[str] = None
    html_url: Optional[str] = None
    followers_url: Optional[str] = None
    following_url: Optional[str] = None
    gists_url: Optional[str] = None
    starred_url: Optional[str] = None
    subscriptions_url: Optional[str] = None
    organizations_url: Optional[str] = None
    repos_url: Optional[str] = None
    events_url: Optional[str] = None
    received_events_url: Optional[str] = None
    type: Optional[str] = None
    site_admin: Optional[bool] = None
    user_view_type: Optional[str] = None


class IGitHubUsers(IGitHubUser, BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    hireable: Optional[bool] = None
    bio: Optional[str] = None
    twitter_username: Optional[str] = None
    public_repos: Optional[int] = None
    public_gists: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
