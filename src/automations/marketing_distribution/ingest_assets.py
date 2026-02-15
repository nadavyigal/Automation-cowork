from __future__ import annotations

import csv
import logging
import subprocess
from datetime import date
from pathlib import Path

try:
    from loguru import logger
except ImportError:  # pragma: no cover - fallback for minimal local environments
    logger = logging.getLogger(__name__)

from src.automations.marketing_distribution.schema import SocialPostDraft

REQUIRED_COLUMNS = {
    "post_id",
    "publish_date",
    "locale",
    "platform",
    "account_target",
    "post_copy",
    "utm_url",
    "status",
}
ACTIVE_STATUSES = {"draft", "pending", "approved"}


def _run_git(args: list[str], cwd: Path | None = None) -> None:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {stderr}")


def sync_assets_from_git(force_sync: bool = False) -> Path | None:
    from src.core.config import settings

    repo_url = settings.marketing_assets_repo_url
    if not repo_url:
        return None

    target_dir = Path(settings.marketing_assets_local_dir)
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    if (target_dir / ".git").exists():
        if not force_sync:
            return target_dir
        logger.info("Refreshing marketing assets from git")
        _run_git(["fetch", "origin", settings.marketing_assets_branch], cwd=target_dir)
        _run_git(["checkout", settings.marketing_assets_branch], cwd=target_dir)
        _run_git(["reset", "--hard", f"origin/{settings.marketing_assets_branch}"], cwd=target_dir)
        return target_dir

    logger.info(f"Cloning marketing assets repo to {target_dir}")
    _run_git(
        [
            "clone",
            "--depth",
            "1",
            "--branch",
            settings.marketing_assets_branch,
            repo_url,
            str(target_dir),
        ]
    )
    return target_dir


def resolve_social_sheet_path(force_sync: bool = False) -> Path:
    from src.core.config import settings

    synced_dir = sync_assets_from_git(force_sync=force_sync)

    if synced_dir:
        path = synced_dir / settings.marketing_csv_relative_path
    else:
        candidate = Path(settings.marketing_csv_relative_path)
        path = candidate if candidate.is_absolute() else (Path.cwd() / candidate)

    if not path.exists():
        raise FileNotFoundError(f"Marketing social sheet not found: {path}")
    return path


def parse_social_sheet(path: Path) -> list[SocialPostDraft]:
    rows: list[SocialPostDraft] = []

    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - fieldnames
        if missing:
            raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")

        for raw_row in reader:
            status = (raw_row.get("status") or "").strip().lower()
            if status not in ACTIVE_STATUSES:
                continue

            publish_date_raw = (raw_row.get("publish_date") or "").strip()
            post_copy = (raw_row.get("post_copy") or "").strip()
            utm_url = (raw_row.get("utm_url") or "").strip()
            if not publish_date_raw or not post_copy or not utm_url:
                logger.warning(f"Skipping invalid marketing row: {raw_row.get('post_id')}")
                continue

            rows.append(
                SocialPostDraft(
                    post_id=(raw_row.get("post_id") or "").strip(),
                    publish_date=date.fromisoformat(publish_date_raw),
                    locale=(raw_row.get("locale") or "en").strip().lower(),
                    platform=(raw_row.get("platform") or "").strip().lower(),
                    account_target=(raw_row.get("account_target") or "").strip(),
                    post_copy=post_copy,
                    utm_url=utm_url,
                    status=status,
                )
            )

    return rows


def load_social_posts(for_date: date | None = None, force_sync: bool = False) -> list[SocialPostDraft]:
    sheet_path = resolve_social_sheet_path(force_sync=force_sync)
    posts = parse_social_sheet(sheet_path)
    if for_date is None:
        return posts
    return [post for post in posts if post.publish_date <= for_date]
