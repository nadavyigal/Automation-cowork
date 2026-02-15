from __future__ import annotations

from datetime import date
from pathlib import Path

from src.automations.marketing_distribution.ingest_assets import parse_social_sheet


def _write_csv(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def test_parse_social_sheet_reads_valid_rows(tmp_path: Path):
    csv_path = tmp_path / "social.csv"
    _write_csv(
        csv_path,
        """
post_id,publish_date,locale,platform,account_target,post_copy,utm_url,status
en_li_01,2026-02-16,en,linkedin,personal,Hello world,https://example.com?a=1,draft
en_li_02,2026-02-17,en,linkedin,personal,Skip me,https://example.com?a=2,done
he_x_01,2026-02-18,he,x,main,Shalom,https://example.com?a=3,approved
""",
    )

    rows = parse_social_sheet(csv_path)
    assert len(rows) == 2
    assert rows[0].post_id == "en_li_01"
    assert rows[0].publish_date == date(2026, 2, 16)
    assert rows[1].post_id == "he_x_01"


def test_parse_social_sheet_requires_columns(tmp_path: Path):
    csv_path = tmp_path / "invalid.csv"
    _write_csv(
        csv_path,
        """
post_id,publish_date,locale,platform,account_target,post_copy,status
en_li_01,2026-02-16,en,linkedin,personal,Hello world,draft
""",
    )

    try:
        parse_social_sheet(csv_path)
        raised = False
    except ValueError:
        raised = True

    assert raised is True
