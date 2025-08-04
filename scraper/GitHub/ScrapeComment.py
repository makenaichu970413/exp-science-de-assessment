# Library
from datetime import datetime
import logging
from pydantic import BaseModel, HttpUrl
from concurrent.futures import ThreadPoolExecutor, as_completed

# Utils
from utils.function.FuncFile import export_json_comments
from utils.function.FuncGeneral import get_github_owner_repo
from utils.function.FuncReport import github_report_issue_comment
from utils.function.FuncRequest import check_request_rate, create_session, ethical_delay
from utils.function import FuncDBLogIssueComment as Log
from utils.constant import (
    REQUEST_RETRY_ATTEMPT,
    REQUEST_TIMEOUT,
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_PROCESS,
)
from utils.model.Igithub_issues import IGitHubIssue
from utils.model.Iguthub_comments import IGitHubComment
from utils.model.Sgithub import TGitHubIssueCommentLog


# ? Return Model of "scrape_comments()"
class DScrapeComments(BaseModel):
    data: list[IGitHubComment] = []
    errors: list[str] = []
    output: str | None = None


# ? Props Model of "process_comments()"
class PProcessComments(BaseModel):
    index: int
    url: HttpUrl
    owner_repo: str
    issues_total: int


# ? Return Model of "process_comments()"
class DProcessComments(BaseModel):
    data: list[IGitHubComment] = []
    error: str | None = None


# ? Scrapping Comments per Issue
def process_comments(props: PProcessComments) -> DProcessComments:

    # ? Initialize the result
    result: DProcessComments = DProcessComments()

    i = props.index
    url = props.url
    total = props.issues_total
    owner_repo = props.owner_repo

    # ? Repository Issue Comments Data:
    # ? GET "/repos/{owner}/{repo}/issues/{issues_no}/comments"
    # ? https://api.github.com/repos/Uniswap/v3-core/issues/1049/comments

    # ? Log the record status into "P - PROCESS" in the database table
    Log.upsert(props=TGitHubIssueCommentLog(url=url, status=STATUS_PROCESS))

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
                # print(f'🔎 [{i}/{total}] "{owner_repo}" in "process_comments": \n{temp}')

                # ? Convert the parsed JSON data list into the "IGitHubComment" model list
                data = [IGitHubComment.model_validate(item) for item in temp]

            # ? Update the "data" into current "result.data" list
            result.data = data
            print(
                f'✅ [{i}/{total}] "{owner_repo}" found total of "{len(data)}" comments'
            )

            # ? Critical delay for ethical web scraping before start the next request
            ethical_delay()

            # ? Exit the looping imediately once successfully get the data response
            break

        # ? If anything going wrong at above then go to "Exception" block
        except Exception as err:

            # ? Set & show the "msg_error"
            msg_error = f'❌ [{i}/{total}] FAILED_SCRAPE in "process_comments()" "{owner_repo}" "{url}" : {err}'
            logging.error(msg_error)

            # ? Wait and retry API request again if "attempt" NOT reaching MAX "REQUEST_RETRY_ATTEMPT"
            if attempt < REQUEST_RETRY_ATTEMPT:
                print(f"🔁[{attempt + 1}/{REQUEST_RETRY_ATTEMPT}] RETRYING : {err} ")
                ethical_delay()
                continue

            # ? Set the "msg_error" into "result.error" AFTER reached MAX "REQUEST_RETRY_ATTEMPT"
            result.error = msg_error

    return result


# ? Scrapping All Issues Comments per GitHub Repository
def scrape_comments(owner_repo: str, issues: list[IGitHubIssue]) -> DScrapeComments:

    # ? Initialize the result
    result: DScrapeComments = DScrapeComments()

    # ? Log all NEW records to "P - PENDING" and skip insert if url already existing in table
    Log.insert_batch(issues, STATUS_PENDING)

    # ? Record the "start_time" for Report purpose
    start_time = datetime.now()

    # ? Generate and show Report before start
    github_report_issue_comment(start=start_time, owner_repo=owner_repo, completed=True)

    # ? Get the log records with status
    # ? If "A - PENDING" scrape new records
    # ? If "P - PROCESS" or "F - FAILED" re-scrape records again
    status = [STATUS_PENDING, STATUS_PROCESS, STATUS_FAILED]
    list_issues = Log.load(status=status, owner_repo=owner_repo)

    # ? Count the "total" length of log records
    total = len(list_issues)

    # ? Stop scrapping if "total" length of log records is "0"
    if not total:
        return result

    # ? Replace the "/" into the "_" in "{owner}/{repository}"
    name = owner_repo.replace("/", "_")

    # ? Start Scrapping Comments data from multiple Issues
    for i, item in enumerate(list_issues, start=1):

        url = item.url
        issue_no = item.issue_no
        props = PProcessComments(
            index=i,
            url=url,
            owner_repo=get_github_owner_repo(str(url)),
            issues_total=total,
        )

        try:
            # ? Make API request to get the Comments data per Issue
            result_process_comments = process_comments(props)

            # ? Get "error" from the "process_comments()"
            error = result_process_comments.error

            # ? Insert the "error" into "result.errors" list if found "error" from the "process_comments()"
            if error:
                result.errors.append(error)

                # ? Block to run below code by raise the "error" to "Exception" block
                raise Exception(error)

            # ? Update the "data" into current "result.data" list
            data = result_process_comments.data
            result.data.extend(data)

            # ? Export NEW comments "data" into json and stored it under "temp" folder
            output = export_json_comments(name=name, issue_no=issue_no, data=data)

            # ? Update the "result.output" with the json output path
            result.output = output

            # ? Log the record status into "C - COMPLETED" and "total" comments found per issue
            Log.upsert(
                props=TGitHubIssueCommentLog(
                    url=url, total=len(data), status=STATUS_COMPLETE
                )
            )

        # ? If above raise "error" then go to "Exception" block
        except Exception as err:

            # ? Show the "msg_error"
            logging.error(err)

            # ? Log the record status into "F - FAILED" and "err" message
            Log.upsert(
                props=TGitHubIssueCommentLog(
                    url=url, error=str(err), status=STATUS_FAILED
                )
            )

    # ? Generate and show Report from the log database after Comments data scrapping was Completed
    github_report_issue_comment(start=start_time, owner_repo=owner_repo)

    return result
