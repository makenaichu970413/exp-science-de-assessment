# Library
import re
import warnings
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning


warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)


def get_github_owner_repo(url: str) -> str | None:
    # https://github.com/Uniswap/v3-core
    # https://api.github.com/repos/Uniswap/v3-core/issues/1050/comments

    # print(f'get_github_owner_repo: "{url}"')

    pattern = r"(?:https?://)(?:www\.)?(?:github\.com/|api\.github\.com/repos/)([^/]+)/([^/]+)"
    match = re.search(pattern, url)

    result = None
    if match:
        owner = match.group(1)
        repo = match.group(2)
        result = f"{owner}/{repo}"

    # print(f"get_github_owner_repo: {result}")
    return result


def trim_string(value: str) -> str:
    temp = re.sub(r"\s+", " ", value)  # normalize whitespace
    temp = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", temp)  # remove control characters
    temp = temp.strip()  # remove leading and trailing whitespace
    temp = temp.replace('"', '""')

    return temp


def trim_html_string(value: str) -> str:
    try:
        # "lxml" 3-5x faster than 'html.parser'
        soup = BeautifulSoup(value, "lxml")
    except Exception:
        # "html.parser" slower than "lxml"
        soup = BeautifulSoup(value, "html.parser")
    temp = soup.get_text()
    temp = trim_string(temp)

    return temp
