#!/usr/bin/env python3
"""DECISIONS の ID・参照・日付見出し・未決ダッシュボードを検査する。"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DECISIONS = ROOT / "00-hub" / "DECISIONS_ja.md"
DEFAULT_NOTES = ROOT / "00-hub" / "NOTES_ja.md"
DASHBOARD_HEADING = "## 未確定（起案・保留）"
DECISION_ROW_RE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2}-\d{2})\s*\|")
DECISION_REF_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}-\d{2}\b")
SHORTHAND_REF_RE = re.compile(
    r"(?P<base>\b\d{4}-\d{2}-\d{2}-\d{2})`?\s*/\s*`?-?"
    r"(?P<short>\d{2})(?!\d)"
)
DATE_HEADING_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2})$")
UNRESOLVED_STATE_RE = re.compile(
    r"\|\s*(起案|保留)(?:（[^|\n]*）)?[^|\n]*\|"
)
REVISION_STATE_RE = re.compile(
    r"\|\s*改訂→`?(\d{4}-\d{2}-\d{2}-\d{2})`?(?:（[^|\n]*）)?\s*\|"
)
LEGACY_SHORTHAND_REFERENCES = frozenset(
    {
        ("2026-06-20-05", "2026-06-20-02"),
        ("2026-06-23-01", "2026-06-19-06"),
        ("2026-07-04-03", "2026-07-04-02"),
        ("2026-07-10-03", "2026-07-03-04"),
        ("2026-07-13-01", "2026-07-12-04"),
        ("2026-07-19-05", "2026-07-10-05"),
    }
)


def check_decisions(
    text: str,
    registered_gap_ids: frozenset[str] = frozenset(),
) -> tuple[list[str], dict[str, int]]:
    """文書を検査し、エラー一覧と集計を返す。"""
    lines = text.splitlines()
    errors: list[str] = []

    date_headings = [
        (match.group(1), line_number)
        for line_number, line in enumerate(lines, start=1)
        if (match := DATE_HEADING_RE.match(line))
    ]
    date_heading_counts = Counter(date for date, _ in date_headings)
    for date, count in sorted(date_heading_counts.items()):
        if count > 1:
            line_numbers = [
                str(line_number)
                for heading_date, line_number in date_headings
                if heading_date == date
            ]
            errors.append(
                f"日付見出し重複: {date} ({count}件、行 {', '.join(line_numbers)})"
            )

    heading_lines = [
        index for index, line in enumerate(lines) if line.strip() == DASHBOARD_HEADING
    ]
    if len(heading_lines) != 1:
        errors.append(
            f"未決ダッシュボード見出しが1件ではありません: {len(heading_lines)}件"
        )
        dashboard_start = dashboard_end = -1
    else:
        dashboard_start = heading_lines[0]
        dashboard_end = next(
            (
                index
                for index in range(dashboard_start + 1, len(lines))
                if lines[index].startswith("## ")
            ),
            len(lines),
        )

    rows: list[tuple[str, int, str]] = []
    for line_number, line in enumerate(lines, start=1):
        match = DECISION_ROW_RE.match(line)
        if match:
            rows.append((match.group(1), line_number, line))

    id_counts = Counter(decision_id for decision_id, _, _ in rows)
    for decision_id, count in sorted(id_counts.items()):
        if count > 1:
            line_numbers = [
                str(line_number)
                for row_id, line_number, _ in rows
                if row_id == decision_id
            ]
            errors.append(
                f"ID重複: {decision_id} ({count}件、行 {', '.join(line_numbers)})"
            )

    unresolved_count = 0
    revision_count = 0
    reference_count = 0
    registered_gap_count = 0
    known_ids = set(id_counts)
    rows_by_id = {decision_id: line for decision_id, _, line in rows}
    for decision_id, line_number, line in rows:
        unresolved_match = UNRESOLVED_STATE_RE.search(line)
        if unresolved_match:
            unresolved_count += 1
            line_index = line_number - 1
            if not (dashboard_start < line_index < dashboard_end):
                errors.append(
                    f"未決行がダッシュボード外にあります: {decision_id} (行 {line_number})"
                )
            if unresolved_match.group(1) == "保留" and "再開トリガ" not in unresolved_match.group(0):
                errors.append(
                    f"保留に再開トリガがありません: {decision_id} (行 {line_number})"
                )

        revision_match = REVISION_STATE_RE.search(line)
        if revision_match:
            revision_count += 1
            target_id = revision_match.group(1)
            if target_id not in known_ids:
                errors.append(
                    f"改訂先が存在しません: {decision_id} -> {target_id} (行 {line_number})"
                )
            elif decision_id not in rows_by_id[target_id]:
                errors.append(
                    "改訂先から旧IDを参照していません: "
                    f"{decision_id} -> {target_id} (行 {line_number})"
                )

        references = set(DECISION_REF_RE.findall(line))
        for shorthand_match in SHORTHAND_REF_RE.finditer(line):
            expanded_id = (
                shorthand_match.group("base").rsplit("-", 1)[0]
                + "-"
                + shorthand_match.group("short")
            )
            references.add(expanded_id)
            if (decision_id, expanded_id) not in LEGACY_SHORTHAND_REFERENCES:
                errors.append(
                    "新規の短縮ID参照は禁止です: "
                    f"{decision_id} -> {shorthand_match.group(0)} (行 {line_number})"
                )

        references.discard(decision_id)
        reference_count += len(references)
        for reference_id in sorted(references):
            if reference_id in known_ids:
                continue
            if reference_id in registered_gap_ids:
                registered_gap_count += 1
                continue
            errors.append(
                "決定参照先が存在せずNOTESにも登録されていません: "
                f"{decision_id} -> {reference_id} (行 {line_number})"
            )

    return errors, {
        "ids": len(rows),
        "unresolved": unresolved_count,
        "revision_links": revision_count,
        "references": reference_count,
        "registered_gaps": registered_gap_count,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DECISIONS の ID・参照・日付見出し・改訂先・未決ダッシュボードを検査する"
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=DEFAULT_DECISIONS,
        help="検査対象（既定: 00-hub/DECISIONS_ja.md）",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        text = args.path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"FAIL: {args.path}: {error}", file=sys.stderr)
        return 2

    registered_gap_ids: frozenset[str] = frozenset()
    if args.path.resolve() == DEFAULT_DECISIONS.resolve():
        try:
            notes_text = DEFAULT_NOTES.read_text(encoding="utf-8")
        except OSError as error:
            print(f"FAIL: {DEFAULT_NOTES}: {error}", file=sys.stderr)
            return 2
        registered_gap_ids = frozenset(DECISION_REF_RE.findall(notes_text))

    errors, counts = check_decisions(text, registered_gap_ids)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(
        "OK decisions "
        f"ids={counts['ids']} "
        f"unresolved={counts['unresolved']} "
        f"revision-links={counts['revision_links']} "
        f"references={counts['references']} "
        f"registered-gaps={counts['registered_gaps']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
