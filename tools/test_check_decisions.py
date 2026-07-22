"""check-decisions.py の回帰テスト。"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "tools" / "check-decisions.py"


def run_checker(text: str | None = None) -> subprocess.CompletedProcess[str]:
    if text is None:
        return subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    with tempfile.TemporaryDirectory() as directory:
        decisions = Path(directory) / "DECISIONS_ja.md"
        decisions.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(CHECKER), str(decisions)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )


class CheckDecisionsTest(unittest.TestCase):
    def test_repository_decisions_passes(self) -> None:
        result = run_checker()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unresolved=2", result.stdout)

    def test_unresolved_row_outside_dashboard_fails(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |

## ログ
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | 後段に残った起案 | 起案 |
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("未決行がダッシュボード外", result.stderr)

    def test_duplicate_id_and_missing_revision_target_fail(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | 再開条件あり | 保留（再開トリガ＝必要時） |

## ログ
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | 重複 | 改訂→2026-07-20-99 |
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("ID重複", result.stderr)
        self.assertIn("改訂先が存在しません", result.stderr)

    def test_duplicate_date_heading_fails(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |

## 2026-07-20
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | 一つ目 | 確定 |

## 2026-07-20
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-02 | 二つ目 | 確定 |
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("日付見出し重複: 2026-07-20", result.stderr)

    def test_revision_target_without_back_reference_fails(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |

## 2026-07-20
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | 旧決定 | 改訂→2026-07-20-02 |
| 2026-07-20-02 | 旧IDを参照しない新決定 | 確定 |
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("改訂先から旧IDを参照していません", result.stderr)

    def test_unregistered_decision_reference_fails(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |

## 2026-07-20
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | `2026-07-20-99`を参照 | 確定 |
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("決定参照先が存在せずNOTESにも登録されていません", result.stderr)

    def test_new_shorthand_reference_fails(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |

## 2026-07-20
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | `2026-07-20-02/03`を参照 | 確定 |
| 2026-07-20-02 | 二つ目 | 確定 |
| 2026-07-20-03 | 三つ目 | 確定 |
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("新規の短縮ID参照は禁止です", result.stderr)

    def test_park_without_resume_trigger_fails(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | 曖昧な棚上げ | 保留 |

## ログ
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("保留に再開トリガがありません", result.stderr)

    def test_decorated_park_state_is_counted(self) -> None:
        result = run_checker(
            """# decisions
## 未確定（起案・保留）
| ID | 決定 | 状態 |
| --- | --- | --- |
| 2026-07-20-01 | 補足つき | 保留（再開トリガ＝必要時）。後継起案へ継承 |

## ログ
"""
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unresolved=1", result.stdout)


if __name__ == "__main__":
    unittest.main()
