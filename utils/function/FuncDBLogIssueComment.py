# Library
import sqlite3
import logging

# ? Utils
from utils.constant import DB_FILEPATH, DB_NAME_ISSUE_COMMENT
from utils.function.FuncDB import db_retry_lock
from utils.function.FuncGeneral import get_github_owner_repo
from utils.model.Igithub_issues import IGitHubIssue
from utils.model.Sgithub import TGitHubIssueCommentLog


def init_table() -> bool:
    """Initialize the log database"""

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()
            # Create tables if not exists
            cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {DB_NAME_ISSUE_COMMENT} (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                issue_url UNIQUE,
                issue_no INTEGER,
                total INTEGER,
                owner_repo TEXT,
                error TEXT,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            )

            connection.commit()
            print(f'🗃️  DB "{DB_NAME_ISSUE_COMMENT}" INIT SUCCESSFULLY')
            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB "{DB_NAME_ISSUE_COMMENT}" in "init_table()": {err}')
        return False


def drop_table() -> bool:
    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            # Drop existing tables
            cursor.execute(f"DROP TABLE IF EXISTS {DB_NAME_ISSUE_COMMENT}")

            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "drop_table()": {err}')
        return False


@db_retry_lock
def insert_batch(arr: list[IGitHubIssue], status: str) -> int:

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()
            data = [
                (
                    str(item.comments_url),
                    str(item.url),
                    item.number,
                    get_github_owner_repo(str(item.comments_url)),
                    status,
                )
                for item in arr
            ]
            # print(f"\n\ninsert_batch: {data}")

            cursor.executemany(
                f"""
                INSERT INTO {DB_NAME_ISSUE_COMMENT} (url, issue_url, issue_no, owner_repo, status) 
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(url) DO NOTHING
                """,
                data,
            )
            connection.commit()
            return cursor.rowcount

    except sqlite3.Error as err:
        logging.error(
            f'❌ ERROR_DB "{DB_NAME_ISSUE_COMMENT}" in "insert_batch()": {err}'
        )
        return 0


@db_retry_lock
def upsert(props: TGitHubIssueCommentLog) -> bool:

    url = str(props.url) if props.url else None
    total = props.total
    error = props.error
    status = props.status

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            """
            Upsert operation : INSERT and UPDATE operations in the SQL query.
            """
            cursor.execute(
                f"""
            INSERT INTO {DB_NAME_ISSUE_COMMENT} (url, total, error, status) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET total = ?, error = ?, status = ?, timestamp = CURRENT_TIMESTAMP
            """,
                (url, total, error, status, total, error, status),
            )
            connection.commit()

            # Return True only if a row was actually inserted
            return cursor.rowcount > 0

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB "{DB_NAME_ISSUE_COMMENT}" in "upsert()": {err}')
        return False


@db_retry_lock
def load(
    status: list[str], owner_repo: str | None = None
) -> list[TGitHubIssueCommentLog]:

    data: list[TGitHubIssueCommentLog] = []

    try:
        with sqlite3.connect(DB_FILEPATH) as conn:
            cursor = conn.cursor()

            # Create placeholders for each status in the list
            # Generates ?, ? Dynamically
            placeholders = ", ".join("?" for _ in status)

            if owner_repo:
                params = tuple(status) + (owner_repo,)
                cursor.execute(
                    f"""
                SELECT * FROM {DB_NAME_ISSUE_COMMENT}
                WHERE status IN ({placeholders}) AND owner_repo = ? 
                """,
                    params,  # Pass statuses as separate parameters
                )
            else:
                cursor.execute(
                    f"""
                SELECT * FROM {DB_NAME_ISSUE_COMMENT}
                WHERE status IN ({placeholders})
                """,
                    tuple(status),
                )

            for row in cursor.fetchall():
                data.append(
                    TGitHubIssueCommentLog(
                        id=row[0],
                        url=row[1],
                        issue_url=row[2],
                        issue_no=row[3],
                        total=row[4],
                        owner_repo=row[5],
                        error=row[6],
                        status=row[7],
                        timestamp=row[8],
                    )
                )

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB "{DB_NAME_ISSUE_COMMENT}" in "load()": {err}')

    return data
