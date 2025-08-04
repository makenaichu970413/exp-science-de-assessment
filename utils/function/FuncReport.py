# Library
from datetime import datetime, timedelta
from typing_extensions import runtime

# Utils
from utils.constant import (
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_PROCESS,
    REPORT_LINE_WIDTH,
)
from utils.function import FuncDBLogRepo as LogRepo
from utils.function import FuncDBLogIssue as LogIssue
from utils.function import FuncDBLogIssueComment as LogIssueComment
from utils.model.Sgithub import TGitHubIssueCommentLog, TGitHubIssueLog, TGitHubRepoLog


def get_estimated_remaining(total: int, completed: int, duration: timedelta) -> str:
    # Calculate estimated time remaining

    estimated_remaining = "N/A"

    elapsed_seconds = duration.total_seconds()
    if completed > 0 and elapsed_seconds > 0:
        records_per_second = completed / elapsed_seconds
        remaining_records = total - completed
        estimated_seconds_remaining = (
            remaining_records / records_per_second if records_per_second > 0 else 0
        )
        # Format to HH:MM:SS
        estimated_remaining = str(
            datetime.fromtimestamp(estimated_seconds_remaining).strftime("%H:%M:%S")
        )

    return estimated_remaining


def get_completed_percentage(total: int, completed: int):
    # Calculate percentage completed
    percentage = (completed / total * 100) if total > 0 else 0

    return percentage


def github_report(start: datetime, completed: bool = False) -> str:

    report = github_report_repo(start, completed)
    report = report + github_report_issue(start, completed)
    report = report + github_report_issue_comment(start, completed)

    return report


def github_report_repo(start: datetime, completed: bool = False) -> str:

    title = "All Repositories"
    start_time = start
    current_time = datetime.now()
    total_duration = current_time - start_time

    pending = LogRepo.load([STATUS_PENDING])
    process = LogRepo.load([STATUS_PROCESS])
    complete = LogRepo.load([STATUS_COMPLETE])
    failed = LogRepo.load([STATUS_FAILED])

    records: list[TGitHubRepoLog] = []
    records.extend(pending)
    records.extend(process)
    records.extend(complete)
    records.extend(failed)

    total_records = len(records)
    completed_count = len(complete)
    failed_count = len(failed)
    pending_count = len(pending)
    processing_count = len(process)

    percentage_completed = get_completed_percentage(
        total=total_records, completed=completed_count
    )

    estimated_remaining = get_estimated_remaining(
        total=total_records, completed=completed_count, duration=total_duration
    )

    # Generate report as single string
    report_lines = []
    report_lines.append("\n" + "=" * REPORT_LINE_WIDTH)
    report_lines.append(f"🚀 GitHub Scraping {title} Report".center(20))
    report_lines.append("=" * REPORT_LINE_WIDTH)
    report_lines.append(
        f"⏱️  Report generated at: {current_time.strftime('%Y-%m-%d %I.%M %p')}"
    )
    report_lines.append(f"⏱️  Total duration: {str(total_duration).split('.')[0]}")
    report_lines.append("-" * REPORT_LINE_WIDTH)
    report_lines.append(f"📊 Total repositories: {total_records}")
    report_lines.append(
        f"✅ Completed: {completed_count} ({percentage_completed:.2f}%)"
    )
    report_lines.append(f"❌ Failed: {failed_count}")
    report_lines.append(f"🔄 Processing: {processing_count}")
    report_lines.append(f"⏳ Pending: {pending_count}")
    if not completed:
        report_lines.append("-" * REPORT_LINE_WIDTH)
        report_lines.append(f"⏱️  Estimated time remaining: {estimated_remaining}")
    report_lines.append("=" * REPORT_LINE_WIDTH + "\n")

    report_text = "\n".join(report_lines)

    # Print to console
    print(report_text)

    # Return the text for email or other uses
    return report_text


def github_report_issue(
    start: datetime, completed: bool = False, owner_repo: str | None = None
) -> str:

    title = f'"{owner_repo}" Issues' if owner_repo else "All Issues"

    start_time = start
    current_time = datetime.now()
    total_duration = current_time - start_time

    pending = LogIssue.load(status=[STATUS_PENDING], owner_repo=owner_repo)
    process = LogIssue.load(status=[STATUS_PROCESS], owner_repo=owner_repo)
    complete = LogIssue.load(status=[STATUS_COMPLETE], owner_repo=owner_repo)
    failed = LogIssue.load(status=[STATUS_FAILED], owner_repo=owner_repo)

    records: list[TGitHubIssueLog] = []
    records.extend(pending)
    records.extend(process)
    records.extend(complete)
    records.extend(failed)

    total_records = len(records)
    completed_count = len(complete)
    failed_count = len(failed)
    pending_count = len(pending)
    processing_count = len(process)
    total_issues = sum([item.total for item in complete if item.total])

    percentage_completed = get_completed_percentage(
        total=total_records, completed=completed_count
    )

    estimated_remaining = get_estimated_remaining(
        total=total_records, completed=completed_count, duration=total_duration
    )

    # for i, item in enumerate(records, start=1):
    #     print(f"{i}. {item}")

    # Generate report as single string
    report_lines = []
    report_lines.append("\n" + "=" * REPORT_LINE_WIDTH)
    report_lines.append(f"🚀 GitHub Scraping {title} Report".center(20))
    report_lines.append("=" * REPORT_LINE_WIDTH)
    report_lines.append(
        f"⏱️  Report generated at: {current_time.strftime('%Y-%m-%d %I.%M %p')}"
    )
    report_lines.append(f"⏱️  Total duration: {str(total_duration).split('.')[0]}")
    report_lines.append("-" * REPORT_LINE_WIDTH)
    report_lines.append(f"🚩 Total issues: {total_issues}")
    report_lines.append(f"📊 Total requests: {total_records}")
    report_lines.append(
        f"✅ Completed: {completed_count} ({percentage_completed:.2f}%)"
    )
    report_lines.append(f"❌ Failed: {failed_count}")
    report_lines.append(f"🔄 Processing: {processing_count}")
    report_lines.append(f"⏳ Pending: {pending_count}")

    if not completed:
        report_lines.append("-" * REPORT_LINE_WIDTH)
        report_lines.append(f"⏱️  Estimated time remaining: {estimated_remaining}")
    report_lines.append("=" * REPORT_LINE_WIDTH + "\n")

    report_text = "\n".join(report_lines)

    # Print to console
    print(report_text)

    # Return the text for email or other uses
    return report_text


def github_report_issue_comment(
    start: datetime, completed: bool = False, owner_repo: str | None = None
) -> str:

    title = f'"{owner_repo}" Issues Comments' if owner_repo else "All Issues Comments"

    start_time = start
    current_time = datetime.now()
    total_duration = current_time - start_time

    pending = LogIssueComment.load(status=[STATUS_PENDING], owner_repo=owner_repo)
    process = LogIssueComment.load(status=[STATUS_PROCESS], owner_repo=owner_repo)
    complete = LogIssueComment.load(status=[STATUS_COMPLETE], owner_repo=owner_repo)
    failed = LogIssueComment.load(status=[STATUS_FAILED], owner_repo=owner_repo)

    records: list[TGitHubIssueCommentLog] = []
    records.extend(pending)
    records.extend(process)
    records.extend(complete)
    records.extend(failed)

    total_records = len(records)
    completed_count = len(complete)
    failed_count = len(failed)
    pending_count = len(pending)
    processing_count = len(process)
    total_comments = sum([item.total for item in complete if item.total])

    percentage_completed = get_completed_percentage(
        total=total_records, completed=completed_count
    )

    estimated_remaining = get_estimated_remaining(
        total=total_records, completed=completed_count, duration=total_duration
    )

    # for i, item in enumerate(records, start=1):
    #     print(f"{i}. {item}")

    # Generate report as single string
    report_lines = []
    report_lines.append("\n" + "=" * REPORT_LINE_WIDTH)
    report_lines.append(f"🚀 GitHub Scraping {title} Report".center(20))
    report_lines.append("=" * REPORT_LINE_WIDTH)
    report_lines.append(
        f"⏱️  Report generated at: {current_time.strftime('%Y-%m-%d %I.%M %p')}"
    )
    report_lines.append(f"⏱️  Total duration: {str(total_duration).split('.')[0]}")
    report_lines.append("-" * REPORT_LINE_WIDTH)
    report_lines.append(f"💬 Total comments: {total_comments}")
    report_lines.append(f"📊 Total requests: {total_records}")
    report_lines.append(
        f"✅ Completed: {completed_count} ({percentage_completed:.2f}%)"
    )
    report_lines.append(f"❌ Failed: {failed_count}")
    report_lines.append(f"🔄 Processing: {processing_count}")
    report_lines.append(f"⏳ Pending: {pending_count}")

    if not completed:
        report_lines.append("-" * REPORT_LINE_WIDTH)
        report_lines.append(f"⏱️  Estimated time remaining: {estimated_remaining}")
    report_lines.append("=" * REPORT_LINE_WIDTH + "\n")

    report_text = "\n".join(report_lines)

    # Print to console
    print(report_text)

    # Return the text for email or other uses
    return report_text
