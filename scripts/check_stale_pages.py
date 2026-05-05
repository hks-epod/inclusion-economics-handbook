"""
Walk every .qmd file in the repo, parse its YAML frontmatter, and flag pages
whose `last-reviewed` is older than STALE_THRESHOLD_DAYS (default 365).

For each stale page we open a GitHub issue (or update an existing open one)
labelled `stale-content` and tag the section's CODEOWNERS.

Run via: `python scripts/check_stale_pages.py`
Triggered monthly by .github/workflows/stale-pages.yml
"""

from __future__ import annotations

import os
import sys
import datetime as dt
from pathlib import Path

import frontmatter
from github import Github


REPO_ROOT = Path(__file__).resolve().parents[1]
THRESHOLD_DAYS = int(os.environ.get("STALE_THRESHOLD_DAYS", "365"))
LABEL = "stale-content"
SKIP_DIRS = {"_site", "_partials", "templates", ".quarto", ".github", "scripts"}


def find_qmd_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*.qmd"):
        if any(part in SKIP_DIRS or part.startswith(".") for part in p.relative_to(root).parts):
            continue
        out.append(p)
    return out


def parse_review_date(value) -> dt.date | None:
    if value is None or value == "":
        return None
    if isinstance(value, dt.date):
        return value
    if isinstance(value, dt.datetime):
        return value.date()
    try:
        return dt.date.fromisoformat(str(value).strip())
    except ValueError:
        return None


def is_stale(reviewed: dt.date | None, today: dt.date) -> bool:
    if reviewed is None:
        return True   # treat missing review date as stale
    return (today - reviewed).days > THRESHOLD_DAYS


def issue_title_for(path: Path) -> str:
    return f"[stale] Review: {path.as_posix()}"


def existing_open_issues(repo) -> dict[str, object]:
    out = {}
    for issue in repo.get_issues(state="open", labels=[LABEL]):
        out[issue.title] = issue
    return out


def ensure_label(repo) -> None:
    try:
        repo.get_label(LABEL)
    except Exception:
        repo.create_label(name=LABEL, color="fbca04",
                          description="Pages overdue for review")


def main() -> int:
    token = os.environ["GH_TOKEN"]
    repo_name = os.environ["GH_REPOSITORY"]
    today = dt.date.today()

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    ensure_label(repo)
    open_issues = existing_open_issues(repo)

    flagged = 0
    for path in find_qmd_files(REPO_ROOT):
        post = frontmatter.load(path)
        reviewed = parse_review_date(post.metadata.get("last-reviewed"))
        if not is_stale(reviewed, today):
            continue

        rel = path.relative_to(REPO_ROOT)
        title = issue_title_for(rel)
        owner = post.metadata.get("owner-role", "Unassigned")
        last = reviewed.isoformat() if reviewed else "never recorded"

        body = (
            f"This page is overdue for review.\n\n"
            f"- **Path:** `{rel.as_posix()}`\n"
            f"- **Owner role:** {owner}\n"
            f"- **Last reviewed:** {last}\n"
            f"- **Threshold:** {THRESHOLD_DAYS} days\n\n"
            f"### What to do\n\n"
            f"1. Read the page end-to-end. Update anything inaccurate or out-of-date.\n"
            f"2. Bump the `last-reviewed` field in the frontmatter to today.\n"
            f"3. Open a PR. Reference this issue with `Closes #{{issue_number}}`.\n\n"
            f"If the page should be deleted or archived instead, set "
            f"`status: archived` and explain in your PR.\n"
        )

        if title in open_issues:
            print(f"already open: {title}")
            continue

        repo.create_issue(title=title, body=body, labels=[LABEL])
        print(f"opened: {title}")
        flagged += 1

    print(f"\nFlagged {flagged} stale page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
