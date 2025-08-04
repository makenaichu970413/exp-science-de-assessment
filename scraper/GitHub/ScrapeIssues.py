# Library
from datetime import datetime
import logging
from pydantic import BaseModel


# Utils
from utils.function.FuncFile import export_json_issues, import_json_issues
from utils.function.FuncRequest import check_request_rate, create_session, ethical_delay
from utils.function import FuncDBLogIssue as LogIssue
from utils.constant import (
    GITHUB_MAX_PER_PAGE,
    REQUEST_RETRY_ATTEMPT,
    REQUEST_TIMEOUT,
    DOMAIN_GITHUB,
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PROCESS,
)
from utils.model.Igithub_issues import IGitHubIssue
from utils.function.FuncReport import github_report_issue
from utils.model.Sgithub import TGitHubIssueLog


# ? Return Model of "process_issues_per_page()"
class DProcessIssuesPerPage(BaseModel):
    data: list[IGitHubIssue] = []
    error: str | None = None


# ? Return Model of "scrape_issues()"
class DScrapeIssues(BaseModel):
    data: list[IGitHubIssue] = []
    errors: list[str] = []
    output: str | None = None


# ? Scrapping Issues per Page
def process_issues_per_page(owner_repo: str, page: int) -> DProcessIssuesPerPage:

    # ? Initialize the result
    result: DProcessIssuesPerPage = DProcessIssuesPerPage()

    # ? Repository Issues Data:
    # ? GET "/repos/{owner}/{repo}/issues?state=all&per_page=100&page=1"
    # ? https://api.github.com/repos/Uniswap/v3-core/issues?state=all&per_page=100&page=1
    state = "all"
    per_page = GITHUB_MAX_PER_PAGE
    url = f"{DOMAIN_GITHUB}repos/{owner_repo}/issues?state={state}&per_page={per_page}&page={page}"

    # ? Log the record status into "P - PROCESS" in the database table
    log = TGitHubIssueLog(
        url=url, owner_repo=owner_repo, page=page, status=STATUS_PROCESS
    )
    LogIssue.upsert(log)

    # ? Retry API request if something going wrong within MAX "REQUEST_RETRY_ATTEMPT"
    for attempt in range(REQUEST_RETRY_ATTEMPT):
        try:
            # ? Check rate limit before make API request
            check_request_rate()

            # ? Create the request session with "GITHUB_TOKEN" "User-Agent" etc
            with create_session() as session:

                # ? GET API request with "REQUEST_TIMEOUT"
                res = session.get(url, timeout=REQUEST_TIMEOUT)

                # ? Parsed the response to JSON
                temp = res.json()
                # print(f'🔎 [{page}] "{owner_repo}" in "process_issues_per_page": \n{temp}')

                # ? Convert the parsed JSON data list into the "IGitHubIssue" model list
                data = [IGitHubIssue.model_validate(item) for item in temp]

            # ? Update the "data" into current "result.data" list
            result.data = data
            print(f'✅ [{page}] "{owner_repo}" found total of {len(data)} issues')

            # ? Critical delay for ethical web scraping before start the next request
            ethical_delay()

            # ? Exit the looping imediately once successfully get the data response
            break

        # ? If anything going wrong at above then go to "Exception" block
        except Exception as err:

            # ? Set & show the "msg_error"
            msg_error = f'❌ [{page}] FAILED_SCRAPE in "process_issues_per_page()" "{owner_repo}" "{url}" : {err}'
            logging.error(msg_error)

            # ? Wait and retry API request again if "attempt" NOT reaching MAX "REQUEST_RETRY_ATTEMPT"
            if attempt < REQUEST_RETRY_ATTEMPT:
                print(f"🔁[{attempt + 1}/{REQUEST_RETRY_ATTEMPT}] RETRYING : {err} ")
                ethical_delay()
                continue

            # ? Set the "msg_error" into "result.error" AFTER reached MAX "REQUEST_RETRY_ATTEMPT"
            result.error = msg_error

    # ? If FOUND "result.error" then Log the record status into "F - FAILED" and "error" message
    if result.error:
        log.error = result.error
        log.status = STATUS_FAILED

    # ? If NO "result.error" then Log the record status into "C - COMPLETED" and "total" issues found per page
    else:
        log.total = len(result.data)
        log.status = STATUS_COMPLETE

    # ? Update the log record into the database table
    LogIssue.upsert(log)

    return result


# ? Scrapping All Issues per GitHub Repository
def scrape_issues(owner_repo: str) -> DScrapeIssues:

    # ? Initialize the result
    result: DScrapeIssues = DScrapeIssues()

    # ? Replace the "/" into the "_" in "{owner}/{repository}"
    name = owner_repo.replace("/", "_")

    # ? Record the "start_time" for Report purpose
    start = datetime.now()

    # ? Initiate the page "count"
    count = 1

    # ? Start Scrapping by looping and handle API pagination using "count" until the return response is empty lsit "[]"
    while True:
        # while count <= 3:

        # ? Check and get the existing data from the "temp" folder
        data_existing = import_json_issues(name=name, page=count)

        # ? If "data_existing" is found then SKIP to make API request to GitHub
        if data_existing is not None:
            print(
                f'🗂️  [{count}] "{owner_repo}" found total of {len(data_existing)} issues'
            )

            # ? If the "data_existing" is empty list "[]" then END and exit the looping
            if not len(data_existing):
                break

            # ? Update the "data_existing" into current result "data" list
            result.data.extend(data_existing)

        # ? If "data_existing" is NOT found
        else:

            # ? Make pagination API request to get the Issues data by "page" count
            result_issues_per_page = process_issues_per_page(
                owner_repo=owner_repo, page=count
            )

            # ? Get "error" from the "process_issues_per_page()"
            error = result_issues_per_page.error

            # ? Insert the "error" into "result.errors" list if found "error" from the "process_issues_per_page()"
            if error:
                result.errors.append(error)

            # ? If NO "error" found
            else:
                # ? Update the "data" into current "result.data" list
                data = result_issues_per_page.data
                result.data.extend(data)

                # ? Export NEW Issues "data" into json and stored it under "temp" folder
                output = export_json_issues(name=name, data=data, page=count)

                # ? Update the "result.output" with the json output path
                result.output = output

                # ? If the "data" is empty list "[]" then END and exit the looping
                total = len(data)
                if not total:
                    break

        # ? Increment the page "count" when not "break" from above process and continue the looping until meet the condtion above to break
        count += 1

    # ? Generate and show Report from the log database after Issues data scrapping was Completed
    github_report_issue(start=start, owner_repo=owner_repo)

    return result
