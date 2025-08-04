# Utils
from utils.constant import (
    DB_NAME_REPO,
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_PROCESS,
)
from utils.function import FuncDBLogRepo as Log
from utils.function.FuncFile import extract_urls_from_excel


def read_input() -> list[str]:

    # ? Extract all the GitHub Repositories URLs from the xlsx in "input" folder
    URLs = extract_urls_from_excel("github_urls.xlsx")

    # ? Count the "totalURLs" length
    totalURLs = len(URLs)

    # ? Return "[]" empty list if "totalURLs" length is "0"
    if not totalURLs:
        print("⚠️  No URLs found in Excel file")
        return []

    # ? Log all NEW URLs to "P - PENDING" and skip insert if url already existing in table
    count = Log.insert_batch(URLs, STATUS_PENDING)

    # ? Check how many URLs was inserted
    # ? Display warning message if not inserted "count" is not same with "totalURLs"
    if count != totalURLs:
        print(
            f'⚠️  Only inserted "{count}" from "{totalURLs}" xlsx records into "{DB_NAME_REPO}"'
        )

    # ? Get the log records with status
    # ? If "A - PENDING" scrape new URL
    # ? If "P - PROCESS" or "F - FAILED" re-scrape URL again
    inputs = Log.load([STATUS_PENDING, STATUS_PROCESS, STATUS_COMPLETE, STATUS_FAILED])

    # ? Count the log records "inputs" length
    total = len(inputs)
    if not total:
        print("⚠️  No pending records found")
        return []

    print(f'\n🔗 In "{DB_NAME_REPO}" found total "{total}" record')
    # for i, item in enumerate(inputs, start=1):
    #     print(f"{i}. {item}")

    # ? Extract the URL string from records list into the "list[str]"
    result = [item.url for item in inputs if item.url]

    return result
