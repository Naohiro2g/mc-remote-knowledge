"""list-reopen-conditions.py の回帰テスト。"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LISTER = ROOT / "tools" / "list-reopen-conditions.py"

SAMPLE = """# NOTES

## Inbox

- 2026-09-01 [park] 版に結びついたpark / 説明 / 再開＝b6 GitHub prerelease identity確認後 / 閉じる＝手順を書いた時
- 2026-09-02 [park] 条件の無いpark / 思想の芽で、再開の契機は書いていない
- 2026-09-03 [priority] 優先の行 / 説明 / 再開＝次回の教材設計レビュー / 閉じる＝改訂した時
- 2026-09-06 [park] 半角スラッシュを含む条件 / 説明 / 再開＝b7 tag後のScratch/WireScope次work着手時 / 閉じる＝直した時
- 2026-09-07 [park] 条件を付け直した行 / 説明 / 再開＝b5実装時 / 閉じる＝直した時 / 2026-09-30棚卸し：条件は過ぎていた / 再開＝b9 gateを開くとき
- 2026-09-04 [done] 閉じた行 / 再開＝b5 tag後
- 2026-09-05 [→DEC 2026-09-05-01] 決定へ上げた行 / 再開＝b7 tag後

## Closed（着地済み・完了）

- 2026-08-01 [park] Closed節のpark / 再開＝b3 tag後

## Archive carry-forward gaps

- YYYY-MM-DD [ ] 対象 / 欠けていた判断 / 必要な公開界面 / 閉じる条件
- 2026-07-25 [ ] 未解決のgap / 欠けていた判断 / 公開界面 / 閉じる＝着地した時
- 2026-07-26 [done] 解決したgap / 欠けていた判断 / 公開界面 / 閉じる＝着地した時
"""


def run_lister(text: str, *extra: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        notes = Path(directory) / "NOTES_ja.md"
        notes.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(LISTER), str(notes), *extra],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )


class ListReopenConditionsTest(unittest.TestCase):
    def test_lists_open_rows_with_reopen_conditions(self) -> None:
        result = run_lister(SAMPLE)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2026-09-01 [park] 版に結びついたpark", result.stdout)
        self.assertIn("再開: b6 GitHub prerelease identity確認後", result.stdout)
        self.assertIn("2026-09-02 [park] 条件の無いpark", result.stdout)
        self.assertIn("再開: （書かれていない）", result.stdout)
        self.assertIn("2026-09-03 [priority] 優先の行", result.stdout)
        self.assertIn("2026-07-25 [ ] 未解決のgap", result.stdout)

    def test_keeps_ascii_slash_inside_condition(self) -> None:
        result = run_lister(SAMPLE)

        self.assertIn("再開: b7 tag後のScratch/WireScope次work着手時", result.stdout)

    def test_uses_latest_reopen_condition(self) -> None:
        result = run_lister(SAMPLE)

        self.assertIn("再開: b9 gateを開くとき", result.stdout)
        self.assertNotIn("再開: b5実装時", result.stdout)

    def test_skips_closed_rows_and_template(self) -> None:
        result = run_lister(SAMPLE)

        self.assertNotIn("閉じた行", result.stdout)
        self.assertNotIn("決定へ上げた行", result.stdout)
        self.assertNotIn("Closed節のpark", result.stdout)
        self.assertNotIn("解決したgap", result.stdout)
        self.assertNotIn("YYYY-MM-DD", result.stdout)

    def test_marks_release_tied_conditions(self) -> None:
        result = run_lister(SAMPLE)
        lines = result.stdout.splitlines()

        tied = [line for line in lines if "版に結びついたpark" in line]
        untied = [line for line in lines if "優先の行" in line]
        self.assertEqual(len(tied), 1)
        self.assertEqual(len(untied), 1)
        self.assertTrue(tied[0].startswith("* "), tied[0])
        self.assertTrue(untied[0].startswith("  "), untied[0])

    def test_release_tied_filter(self) -> None:
        result = run_lister(SAMPLE, "--release-tied")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("版に結びついたpark", result.stdout)
        self.assertNotIn("条件の無いpark", result.stdout)
        self.assertNotIn("優先の行", result.stdout)

    def test_default_notes_file_runs(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LISTER)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[park]", result.stdout)


if __name__ == "__main__":
    unittest.main()
