# Library
import sqlite3
import logging

# ? Utils
from utils.constant import DB_FILEPATH, DB_NAME_ISSUE
from utils.function.FuncDB import db_retry_lock
from utils.model.Sgithub import TGitHubIssueLog


def init_table() -> bool:
    """Initialize the log database"""

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()
            # Create tables if not exists
            cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {DB_NAME_ISSUE} (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                owner_repo TEXT,
                page INTEGER,
                total INTEGER,
                error TEXT,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            )

            connection.commit()
            print(f'🗃️  DB "{DB_NAME_ISSUE}" INIT SUCCESSFULLY')
            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB "{DB_NAME_ISSUE}" in "init_table()": {err}')
        return False


def drop_table() -> bool:
    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            # Drop existing tables
            cursor.execute(f"DROP TABLE IF EXISTS {DB_NAME_ISSUE}")

            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "drop_table()": {err}')
        return False


@db_retry_lock
def upsert(props: TGitHubIssueLog) -> bool:

    url = str(props.url) if props.url else None
    owner_repo = props.owner_repo
    page = props.page
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
            INSERT INTO {DB_NAME_ISSUE} (url, owner_repo, page, total, error, status) 
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET owner_repo = ?, page = ?, total = ?, error = ?, status = ?, timestamp = CURRENT_TIMESTAMP
            """,
                (
                    url,
                    owner_repo,
                    page,
                    total,
                    error,
                    status,
                    owner_repo,
                    page,
                    total,
                    error,
                    status,
                ),
            )
            connection.commit()

            # Return True only if a row was actually inserted
            return cursor.rowcount > 0

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB "{DB_NAME_ISSUE}" in "upsert()": {err}')
        return False


@db_retry_lock
def load(status: list[str], owner_repo: str | None = None) -> list[TGitHubIssueLog]:

    data: list[TGitHubIssueLog] = []

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
                SELECT * FROM {DB_NAME_ISSUE}
                WHERE status IN ({placeholders}) AND owner_repo = ? 
                """,
                    params,  # Pass statuses as separate parameters
                )
            else:
                cursor.execute(
                    f"""
                SELECT * FROM {DB_NAME_ISSUE}
                WHERE status IN ({placeholders})
                """,
                    tuple(status),
                )

            for row in cursor.fetchall():
                data.append(
                    TGitHubIssueLog(
                        id=row[0],
                        url=row[1],
                        owner_repo=row[2],
                        page=row[3],
                        total=row[4],
                        error=row[5],
                        status=row[6],
                        timestamp=row[7],
                    )
                )

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB "{DB_NAME_ISSUE}" in "load()": {err}')

    return data
