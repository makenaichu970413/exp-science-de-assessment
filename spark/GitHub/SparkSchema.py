# Library
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    ArrayType,
    IntegerType,
    BooleanType,
    TimestampType,
    MapType,
)


def schema_user() -> StructType:
    return StructType(
        [
            StructField("login", StringType(), True),
            StructField("id", IntegerType(), True),
            StructField("node_id", StringType(), True),
            StructField("avatar_url", StringType(), True),
            StructField("gravatar_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("followers_url", StringType(), True),
            StructField("following_url", StringType(), True),
            StructField("gists_url", StringType(), True),
            StructField("starred_url", StringType(), True),
            StructField("subscriptions_url", StringType(), True),
            StructField("organizations_url", StringType(), True),
            StructField("repos_url", StringType(), True),
            StructField("events_url", StringType(), True),
            StructField("received_events_url", StringType(), True),
            StructField("type", StringType(), True),
            StructField("site_admin", BooleanType(), True),
            StructField("user_view_type", StringType(), True),
        ]
    )


def schema_label() -> StructType:
    return StructType(
        [
            StructField("id", IntegerType(), True),
            StructField("node_id", StringType(), True),
            StructField("url", StringType(), True),
            StructField("name", StringType(), True),
            StructField("color", StringType(), True),
            StructField("default", BooleanType(), True),
            StructField("description", StringType(), True),
        ]
    )


def schema_milestone() -> StructType:
    return StructType(
        [
            StructField("url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("labels_url", StringType(), True),
            StructField("id", IntegerType(), True),
            StructField("node_id", StringType(), True),
            StructField("number", IntegerType(), True),
            StructField("title", StringType(), True),
            StructField("description", StringType(), True),
            StructField("creator", schema_user(), True),
            StructField("open_issues", IntegerType(), True),
            StructField("closed_issues", IntegerType(), True),
            StructField("state", StringType(), True),
            StructField("created_at", TimestampType(), True),
            StructField("updated_at", TimestampType(), True),
            StructField("due_on", TimestampType(), True),
            StructField("closed_at", TimestampType(), True),
        ]
    )


def schema_issue_type() -> StructType:
    return StructType(
        [
            StructField("id", IntegerType(), True),
            StructField("node_id", StringType(), True),
            StructField("name", StringType(), True),
            StructField("description", StringType(), True),
            StructField("color", StringType(), True),
            StructField("created_at", TimestampType(), True),
            StructField("updated_at", TimestampType(), True),
            StructField("is_enabled", BooleanType(), True),
        ]
    )


def schema_sub_issue_summary() -> StructType:
    return StructType(
        [
            StructField("total", IntegerType(), True),
            StructField("completed", IntegerType(), True),
            StructField("percent_completed", IntegerType(), True),
        ]
    )


def schema_reactions() -> StructType:
    return StructType(
        [
            StructField("url", StringType(), True),
            StructField("total_count", IntegerType(), True),
            StructField("plus1", IntegerType(), True),
            StructField("minus1", IntegerType(), True),
            StructField("laugh", IntegerType(), True),
            StructField("hooray", IntegerType(), True),
            StructField("confused", IntegerType(), True),
            StructField("heart", IntegerType(), True),
            StructField("rocket", IntegerType(), True),
            StructField("eyes", IntegerType(), True),
        ]
    )


def schema_pull_request() -> StructType:
    return StructType(
        [
            StructField("url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("diff_url", StringType(), True),
            StructField("patch_url", StringType(), True),
            StructField("merged_at", TimestampType(), True),
        ]
    )


def schema_app() -> StructType:
    return StructType(
        [
            StructField("id", IntegerType(), True),
            StructField("client_id", StringType(), True),
            StructField("slug", StringType(), True),
            StructField("node_id", StringType(), True),
            StructField("owner", schema_user(), True),
            StructField("name", StringType(), True),
            StructField("description", StringType(), True),
            StructField("external_url", StringType(), True),
            StructField("html_url", StringType(), True),
            StructField("created_at", StringType(), True),
            StructField("updated_at", StringType(), True),
            StructField("permissions", MapType(StringType(), StringType()), True),
            StructField("events", ArrayType(StringType()), True),
        ]
    )


def schema_issue():
    return {
        # Complex Schema
        "user": schema_user(),
        "labels": ArrayType(schema_label()),
        "assignee": schema_user(),
        "assignees": ArrayType(schema_user()),
        "milestone": schema_milestone(),
        "closed_by": schema_user(),
        "reactions": schema_reactions(),
        "pull_request": schema_pull_request(),
        "sub_issues_summary": schema_sub_issue_summary(),
        "type": schema_issue_type(),
        # Simple Schema
        "url": StringType(),
        "repository_url": StringType(),
        "labels_url": StringType(),
        "comments_url": StringType(),
        "events_url": StringType(),
        "html_url": StringType(),
        "id": IntegerType(),
        "node_id": StringType(),
        "number": IntegerType(),
        "title": StringType(),
        "state": StringType(),
        "locked": BooleanType(),
        "comments": IntegerType(),
        "created_at": TimestampType(),
        "updated_at": TimestampType(),
        "closed_at": TimestampType(),
        "author_association": StringType(),
        "active_lock_reason": StringType(),
        "body": StringType(),
        "timeline_url": StringType(),
        "performed_via_github_app": StringType(),
        "state_reason": StringType(),
        "draft": BooleanType(),
    }


def schema_comment():
    return {
        # Complex Schema
        "user": schema_user(),
        "reactions": schema_reactions(),
        "performed_via_github_app": schema_app(),
        # Simple Schema
        "url": StringType(),
        "html_url": StringType(),
        "issue_url": StringType(),
        "node_id": StringType(),
        "author_association": StringType(),
        "body": StringType(),
        "id": IntegerType(),
        "created_at": TimestampType(),
        "updated_at": TimestampType(),
    }
