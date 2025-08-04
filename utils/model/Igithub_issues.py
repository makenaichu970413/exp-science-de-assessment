# Library
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl

# Utils
from utils.model.Igithub_users import IGitHubUser


class IGitHubIssueLabel(BaseModel):
    id: Optional[int] = None
    node_id: Optional[str] = None
    url: Optional[HttpUrl] = None
    name: Optional[str] = None
    color: Optional[str] = None
    default: Optional[bool] = None
    description: Optional[str] = None


class IGitHubMilestone(BaseModel):
    url: Optional[HttpUrl] = None
    html_url: Optional[HttpUrl] = None
    labels_url: Optional[HttpUrl] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    number: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    creator: Optional[IGitHubUser] = None
    open_issues: Optional[int] = None
    closed_issues: Optional[int] = None
    state: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    due_on: Optional[datetime] = None
    closed_at: Optional[datetime] = None


class IGitHubReactions(BaseModel):
    url: Optional[HttpUrl] = None
    total_count: Optional[int] = None
    plus1: Optional[int] = Field(alias="+1", default=None)
    minus1: Optional[int] = Field(alias="-1", default=None)
    laugh: Optional[int] = None
    hooray: Optional[int] = None
    confused: Optional[int] = None
    heart: Optional[int] = None
    rocket: Optional[int] = None
    eyes: Optional[int] = None

    class Config:
        # This will use the alias names during serialization
        validate_by_name = True
        json_encoders = {
            # Add any custom type encoding here if needed
        }


class IGitHubSubIssuesSummary(BaseModel):
    total: Optional[int] = None
    completed: Optional[int] = None
    percent_completed: Optional[int] = None


class IGitHubPullRequest(BaseModel):
    url: Optional[HttpUrl] = None
    html_url: Optional[HttpUrl] = None
    diff_url: Optional[HttpUrl] = None
    patch_url: Optional[HttpUrl] = None
    merged_at: Optional[datetime] = None


class IGitHubIssueType(BaseModel):
    id: Optional[int] = None
    node_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_enabled: Optional[bool] = None


class IGitHubIssue(BaseModel):
    url: Optional[HttpUrl] = None
    repository_url: Optional[HttpUrl] = None
    labels_url: Optional[HttpUrl] = None
    comments_url: Optional[HttpUrl] = None
    events_url: Optional[HttpUrl] = None
    html_url: Optional[HttpUrl] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    number: Optional[int] = None
    title: Optional[str] = None
    user: Optional[IGitHubUser] = None
    labels: Optional[List[IGitHubIssueLabel]] = None
    state: Optional[str] = None
    locked: Optional[bool] = None
    assignee: Optional[IGitHubUser] = None
    assignees: Optional[List[IGitHubUser]] = None
    milestone: Optional[IGitHubMilestone] = None
    comments: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    author_association: Optional[str] = None
    type: Optional[IGitHubIssueType] = None
    active_lock_reason: Optional[str] = None
    sub_issues_summary: Optional[IGitHubSubIssuesSummary] = None
    body: Optional[str] = None
    closed_by: Optional[IGitHubUser] = None
    reactions: Optional[IGitHubReactions] = None
    timeline_url: Optional[HttpUrl] = None
    performed_via_github_app: Optional[str] = None
    state_reason: Optional[str] = None
    draft: Optional[bool] = None
    pull_request: Optional[IGitHubPullRequest] = None
