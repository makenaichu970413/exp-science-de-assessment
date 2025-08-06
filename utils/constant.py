# Library
import os
from pathlib import Path
from dotenv import load_dotenv


# Load Environment
load_dotenv()


REQUEST_RETRY_ATTEMPT = 3
REQUEST_MAX_PER_MINUTE = 3  #! GITHUB MAX 5000 per Hour
REQUEST_PAUSES_SECOND = 30
REQUEST_TIMEOUT = 10  # second


GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")
GITHUB_API_VERSION = "2022-11-28"  #! GITHUB API Latest version
GITHUB_MAX_PER_PAGE = 100


JAVA_HOME: str | None = os.getenv("JAVA_HOME")
HADOOP_HOME: str | None = os.getenv("HADOOP_HOME")


BRIGHTDATA_ZONE: str | None = os.getenv("BRIGHTDATA_ZONE")
BRIGHTDATA_USER: str | None = os.getenv("BRIGHTDATA_USER")
BRIGHTDATA_PASS: str | None = os.getenv("BRIGHTDATA_PASS")
OS_BRIGHTDATA_PORT: str | None = os.getenv("BRIGHTDATA_PORT")
BRIGHTDATA_PORT: int | None = int(OS_BRIGHTDATA_PORT) if OS_BRIGHTDATA_PORT else None


OS_PROXY: str | None = os.getenv("PROXY")
PROXY: list[str] = OS_PROXY.split(",") if OS_PROXY else []


FOLDER_ROOT = Path(__file__).parent.parent.as_posix()
FOLDER_OUTPUT = f"{FOLDER_ROOT}/output"
FOLDER_INPUT = f"{FOLDER_ROOT}/input"
FOLDER_LOG = f"{FOLDER_ROOT}/log"
FOLDER_TEMP = f"{FOLDER_ROOT}/temp"
FOLDER_SQL = f"{FOLDER_ROOT}/sql"
FOLDER_SPARK = f"{FOLDER_ROOT}/spark"
FOLDER_SPARK_TEMP = f"{FOLDER_SPARK}/temp"


DB_NAME = "github_logs"
DB_FILEPATH = f"{FOLDER_LOG}/{DB_NAME}.db"
DB_NAME_REPO = f"{DB_NAME}_repo"
DB_NAME_ISSUE = f"{DB_NAME}_issue"
DB_NAME_ISSUE_COMMENT = f"{DB_NAME}_issue_comment"


STATUS_PENDING = "P"
STATUS_PROCESS = "A"
STATUS_COMPLETE = "C"
STATUS_FAILED = "F"


REPORT_LINE_WIDTH = 70


DOMAIN_GITHUB = "https://api.github.com/"
