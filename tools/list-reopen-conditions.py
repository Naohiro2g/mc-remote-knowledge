#!/usr/bin/env python3
"""hub NOTES の未着地の行から再開条件を抜き出して一覧にする。

gate を開くときと閉じるときに回す（`2026-09-30-09`）。判定はしない。再開条件が
release、component、gate に結びついていそうな行に `*` を付けるだけで、条件が
来ているかは人と coordinator が決める。
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NOTES = ROOT / "00-hub" / "NOTES_ja.md"

INBOX_HEADING = "## Inbox"
GAPS_HEADING = "## Archive carry-forward gaps"
OPEN_TAGS = {"park", "priority", "candidate", "future", " "}

ROW_RE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) \[([^\]]*)\] (.*)$")
# NOTES の区切りは前後に空白のある " / "。条件の中の半角 "/" では切らない。
REOPEN_RE = re.compile(r"再開[＝=]\s*(.*?)(?: / |$)")
RELEASE_TIED_RE = re.compile(
    r"\bb\d+\b|\brc\d*\b|stable|gate|tag|release|リリース|公開|実装",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class OpenRow:
    date: str
    tag: str
    title: str
    reopen: str | None

    @property
    def release_tied(self) -> bool:
        return self.reopen is not None and bool(RELEASE_TIED_RE.search(self.reopen))


def parse_open_rows(text: str) -> list[OpenRow]:
    rows: list[OpenRow] = []
    section: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line.strip()
            continue
        if section not in (INBOX_HEADING, GAPS_HEADING):
            continue
        match = ROW_RE.match(line)
        if match is None:
            continue
        date, tag, rest = match.groups()
        if tag not in OPEN_TAGS:
            continue
        title = rest.split(" / ", 1)[0].strip()
        # 棚卸しで条件を付け直すときは行末へ追記するので、最後の「再開＝」を使う。
        reopen_matches = REOPEN_RE.findall(rest)
        reopen = reopen_matches[-1].strip() if reopen_matches else None
        rows.append(OpenRow(date=date, tag=tag, title=title, reopen=reopen or None))
    return rows


def format_row(row: OpenRow) -> str:
    mark = "*" if row.release_tied else " "
    reopen = row.reopen if row.reopen is not None else "（書かれていない）"
    return f"{mark} {row.date} [{row.tag}] {row.title}\n      再開: {reopen}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="hub NOTES の未着地の行（park／priority／candidate／future、archive gap）の再開条件を一覧にする"
    )
    parser.add_argument("notes", nargs="?", type=Path, default=DEFAULT_NOTES)
    parser.add_argument(
        "--release-tied",
        action="store_true",
        help="再開条件がrelease、component、gateに結びついていそうな行（*）だけを出す",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = parse_open_rows(args.notes.read_text(encoding="utf-8"))
    if args.release_tied:
        rows = [row for row in rows if row.release_tied]
    for row in rows:
        print(format_row(row))
    tied = sum(1 for row in rows if row.release_tied)
    print(f"\n{len(rows)} rows, release-tied={tied}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
