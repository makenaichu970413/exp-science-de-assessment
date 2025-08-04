# Library
import sqlite3
import logging
import json

# ? Utils
from utils.constant import DB_FILEPATH, DB_NAME_REPO
from utils.function.FuncDB import db_retry_lock
from utils.model.Sgithub import TGitHubRepoLog, TGitHubRepoOutput


def init_table() -> bool:
    """Initialize the log database"""

    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()
            # Create tables if not exists
            cursor.execute(
                f"""
            CREATE TABLE IF NOT EXISTS {DB_NAME_REPO} (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                output JSON,
                error TEXT,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
            )

            connection.commit()
            print(f'🗃️  DB "{DB_NAME_REPO}" INIT SUCCESSFULLY')
            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "init_table()": {err}')
        return False


def drop_table() -> bool:
    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()

            # Drop existing tables
            cursor.execute(f"DROP TABLE IF EXISTS {DB_NAME_REPO}")

            return True

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "drop_table()": {err}')
        return False


@db_retry_lock
def insert_batch(urls: list[str], status: str) -> int:
    try:
        with sqlite3.connect(DB_FILEPATH) as connection:
            cursor = connection.cursor()
            data = [(url, status) for url in urls]
            cursor.executemany(
                f"""
                INSERT INTO {DB_NAME_REPO} (url, status) 
                VALUES (?, ?)
                ON CONFLICT(url) DO NOTHING
                """,
                data,
            )
            connection.commit()
            return cursor.rowcount

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "insert_batch()": {err}')
        return 0


@db_retry_lock
def upsert(props: TGitHubRepoLog) -> bool:

    url = props.url
    output = props.output.model_dump_json()  # Convert output to JSON string
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
            INSERT INTO {DB_NAME_REPO} (url, output, error, status) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET output = ?, error = ?, status = ?, timestamp = CURRENT_TIMESTAMP
            """,
                (
                    url,
                    output,
                    error,
                    status,
                    output,
                    error,
                    status,
                ),
            )
            connection.commit()

            # Return True only if a row was actually inserted
            return cursor.rowcount > 0

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "upsert()": {err}')
        return False


@db_retry_lock
def load(status: list[str]) -> list[TGitHubRepoLog]:

    data: list[TGitHubRepoLog] = []

    try:
        with sqlite3.connect(DB_FILEPATH) as conn:
            cursor = conn.cursor()

            # Create placeholders for each status in the list
            # Generates ?, ? Dynamically
            placeholders = ", ".join("?" for _ in status)

            cursor.execute(
                f"""
            SELECT * FROM {DB_NAME_REPO}
            WHERE status IN ({placeholders})
            """,
                tuple(status),  # Pass statuses as separate parameters
            )

            for row in cursor.fetchall():
                temp = row[2]
                output = TGitHubRepoOutput()
                if temp:
                    try:
                        parsed = json.loads(temp)
                        output = TGitHubRepoOutput.model_validate(parsed)
                    except Exception as e:
                        logging.error(f"ERROR TGitHubRepoOutput: {e}")

                data.append(
                    TGitHubRepoLog(
                        id=row[0],
                        url=row[1],
                        output=output,
                        error=row[3],
                        status=row[4],
                        timestamp=row[5],
                    )
                )

    except sqlite3.Error as err:
        logging.error(f'❌ ERROR_DB in "load()": {err}')

    return data
