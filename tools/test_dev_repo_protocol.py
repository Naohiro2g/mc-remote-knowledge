"""dev-agent runtime blockの配布内容を検査する。"""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = ROOT / "00-hub" / "dev-repo-protocol_ja.md"
BEGIN = "<!-- BEGIN: DEV-AGENT-RUNTIME -->"
END = "<!-- END: DEV-AGENT-RUNTIME -->"


def runtime_block() -> str:
    lines = PROTOCOL.read_text(encoding="utf-8").splitlines()
    begin = [index for index, line in enumerate(lines) if line == BEGIN]
    end = [index for index, line in enumerate(lines) if line == END]

    if len(begin) != 1 or len(end) != 1 or begin[0] >= end[0]:
        raise AssertionError("dev-agent runtime marker missing, duplicated, or reversed")

    return "\n".join(lines[begin[0] + 1 : end[0]])


class DevRepoProtocolTest(unittest.TestCase):
    def test_runtime_block_contains_local_notes_boundary(self) -> None:
        block = runtime_block()

        self.assertIn("`CLAUDE.md`と`NOTES_ja.md`は運用者ローカル限定", block)
        self.assertIn("`.gitignore`へ追加", block)
        self.assertIn("stage、commit、pushしない", block)
        self.assertIn("push前に停止して状態を報告", block)


if __name__ == "__main__":
    unittest.main()
