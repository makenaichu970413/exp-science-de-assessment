# Library
from typing import Dict
from pydantic import BaseModel, HttpUrl

from utils.model.Igithub_issues import IGitHubIssue
from utils.model.Iguthub_comments import IGitHubComment


class TGitHubRepoOutput(BaseModel):
    issues: str | None = None
    issues_comments: str | None = None


class TGitHubRepoLog(BaseModel):
    id: int | None = None
    url: str | None = None
    output: TGitHubRepoOutput = TGitHubRepoOutput()
    error: str | None = None
    status: str | None = None
    timestamp: str | None = None


class TGitHubIssueLog(BaseModel):
    id: int | None = None
    url: HttpUrl | None = None  # issues_url
    owner_repo: str | None = None
    page: int | None = None
    total: int | None = None  # total issues
    error: str | None = None
    status: str | None = None
    timestamp: str | None = None


class TGitHubIssueCommentLog(BaseModel):
    id: int | None = None
    url: HttpUrl | None = None  # comments_url
    issue_url: HttpUrl | None = None
    issue_no: int | None = None
    total: int | None = None
    owner_repo: str | None = None
    error: str | None = None
    status: str | None = None
    timestamp: str | None = None


TGitHubIssueExport = Dict[str, Dict[str, list[IGitHubIssue]]]


TGitHubIssueCommentExport = Dict[str, list[IGitHubComment]]
