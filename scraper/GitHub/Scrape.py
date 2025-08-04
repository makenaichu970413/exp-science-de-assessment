# Library
from datetime import datetime
from pydantic import BaseModel

# Scraper
from scraper.GitHub.ScrapeInit import read_input
from scraper.GitHub.ScrapeComment import scrape_comments
from scraper.GitHub.ScrapeIssues import scrape_issues

# Utils
from utils.constant import STATUS_COMPLETE, STATUS_PROCESS
from utils.function.FuncFile import export_csv_comments, export_csv_issues
from utils.function.FuncGeneral import get_github_owner_repo
from utils.function import FuncDBLogRepo as LogRepo
from utils.function import FuncDBLogIssue as LogIssue
from utils.function import FuncDBLogIssueComment as LogIssueComment
from utils.function.FuncReport import github_report
from utils.model.Sgithub import TGitHubRepoLog, TGitHubRepoOutput


# ? Props Model of "process_github()"
class PProcessGitHub(BaseModel):
    url: str
    index: int
    total: int


# ? Return Model of "process_github()"
class DProcessGitHub(BaseModel):
    output: TGitHubRepoOutput = TGitHubRepoOutput()
    error: str | None = None


# ? Scrapping Issues & Comments per GitHub Repository
def process_github(props: PProcessGitHub) -> DProcessGitHub:

    # ? Getting the "url" "i" "total" from props
    url = props.url
    i = props.index
    total = props.total

    # ? Initialize the result
    result: DProcessGitHub = DProcessGitHub()

    # ? Get the "owner" & "repository" name from URL
    owner_repo = get_github_owner_repo(url)

    # ? Replace the "/" into the "_" in "{owner}/{repository}"
    name = owner_repo.replace("/", "_")

    # ? If "{owner}/{repository}" not found from URL then return the result with None "output"
    if not owner_repo:
        print(f'Not Found "owner_repo" !')
        return result

    # ? Log the record status into "P - PROCESS" in the database table
    LogRepo.upsert(TGitHubRepoLog(url=url, status=STATUS_PROCESS))

    # ? Scrapping Start
    print(f'\n\n🤖 [{i}/{total}] Scrapping "{url}" ...')

    # ? Collect ALL the Issues data from GitHub repository
    result_issue = scrape_issues(owner_repo)

    # ? Export Issues data into csv
    result.output.issues = export_csv_issues(name)

    # ? Filter out the Issues data with "comments" field have "0" value
    data_issue = result_issue.data
    data_issue = [item for item in data_issue if item.comments]

    #! Test
    # data_issue = data_issue[:5]
    # data_issue = []

    # ? Get ALL the Comments data from above Issues data
    result_comments = scrape_comments(owner_repo=owner_repo, issues=data_issue)

    # ? Export Comments data into csv
    result.output.issues_comments = export_csv_comments(name)

    # ? Scrapping End
    print(f'✅ [{i}/{total}] Scrapping "{url}": {result}')

    return result


# ? Root function of Scraping GitHub data
def run() -> None:

    # ? Initialize the database
    bool1 = LogRepo.init_table()
    bool2 = LogIssue.init_table()
    bool3 = LogIssueComment.init_table()
    isInitDB = bool1 and bool2 and bool3

    # ? Stop scrapping if one of the database from above is failed to initialize
    if not isInitDB:
        return

    # ? Read and get the URLs from the log database
    URLs = read_input()

    # ? Record the "start_time" for Report purpose
    start_time = datetime.now()

    # ? Count the "total" length of URLs
    total = len(URLs)

    # ? Stop scrapping if "total" length of URLs is "0"
    if not total:
        # ? Generate and show Report from the log database
        github_report(start_time, completed=True)
        return

    # ? Start Scrapping by looping the "url" item one by one from "URLs"
    for i, url in enumerate(URLs, start=1):

        # ? Start Scrapping Issues & Comments by passing props(url, i, total)
        result = process_github(props=PProcessGitHub(url=url, index=i, total=total))

        # ? Record the output path of csv file for exported Issues & Comments data
        output = result.output

        # ? Log the record status into "P - COMPLETE" in the database table
        LogRepo.upsert(TGitHubRepoLog(url=url, status=STATUS_COMPLETE, output=output))

    # ? Generate and show Report from the log database after ALL scrapping was Completed
    github_report(start_time, completed=True)
