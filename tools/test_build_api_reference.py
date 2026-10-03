"""build-api-reference.py の回帰テスト。"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUILDER = ROOT / "tools" / "build-api-reference.py"

WIRE = """# wire

## 4. コマンド表（確定）

| method | params（位置） | 応答 | 備考 |
| --- | --- | --- | --- |
| `hello` | object（§6） | あり | 接続ハンドシェイク |
| `world.setBlock` | `[x, y, z, blockSpec]` | id付きは`null` | 1ブロック設置（§7.1） |
| `world.playSound` | `[x, y, z, sound_id, (options)]` | `null` | 位置から音を鳴らす（b8、§5.8.3） |
| `events.clear` | 後続contractで固定 | あり | 候補 |

## 5. 次の節

### 7.3 エラー設計

| family | code | reason | 意味 | 導入 |
| --- | --- | --- | --- | --- |
| params 検証 | `-32602`（Invalid params） | `invalid_params` | 形が不正 | b2 |
| | | `zero_direction` | 向きが無い | b7 |
| resource-ref | `-32602` | `unknown_sound` | 未登録の音 | b8 |

- 表の後の説明
"""

META = {
    "schema": "mc-remote.api-reference-metadata",
    "schema_version": 1,
    "release": {"label": "b8", "protocol": "23.2.0", "artifact": "2320.0.0b8", "minecraft": "1.21.11", "published": "2026-10-03"},
    "categories": [{"id": "connection", "title": "接続"}, {"id": "block", "title": "ブロック"}, {"id": "effect", "title": "演出"}],
    "methods": [
        {"method": "hello", "category": "connection", "purpose": "最初に送る"},
        {"method": "world.setBlock", "category": "block", "purpose": "ブロックを置く"},
        {"method": "world.playSound", "category": "effect", "purpose": "音を鳴らす"},
    ],
    "excluded": [{"method": "events.clear", "reason": "候補"}],
    "auth": {"wire_sections": "§6.5", "methods": [{"method": "auth.pairBegin", "purpose": "ペアリングを始める"}]},
}


def run(meta: dict, wire: str = WIRE, *extra: str) -> tuple[subprocess.CompletedProcess[str], Path]:
    directory = Path(tempfile.mkdtemp())
    (directory / "wire.md").write_text(wire, encoding="utf-8")
    (directory / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    out = directory / "out"
    result = subprocess.run(
        [sys.executable, str(BUILDER), "--wire", str(directory / "wire.md"), "--metadata", str(directory / "meta.json"), "--out", str(out), *extra],
        cwd=ROOT, check=False, capture_output=True, text=True,
    )
    return result, out


class BuildApiReferenceTest(unittest.TestCase):
    def test_generates_html_and_json(self) -> None:
        result, out = run(META)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((out / "api.json").read_text(encoding="utf-8"))
        names = [m["method"] for m in data["methods"]]
        self.assertEqual(names, ["hello", "world.setBlock", "world.playSound"])
        sound = data["methods"][2]
        self.assertEqual(sound["params"], "`[x, y, z, sound_id, (options)]`")
        self.assertNotIn("since", sound)
        self.assertEqual(sound["notes"], "位置から音を鳴らす（b8、§5.8.3）")
        self.assertEqual(sound["category"], "effect")
        self.assertEqual([e["reason"] for e in data["errors"]], ["invalid_params", "zero_direction", "unknown_sound"])
        self.assertEqual(data["errors"][1]["family"], "params 検証")
        html = (out / "index.html").read_text(encoding="utf-8")
        self.assertIn("<code>world.playSound</code>", html)
        self.assertIn("音を鳴らす", html)
        self.assertIn("auth.pairBegin", html)
        self.assertNotIn("events.clear", html)

    def test_fails_when_table_has_unlisted_method(self) -> None:
        meta = json.loads(json.dumps(META))
        meta["excluded"] = []
        result, _ = run(meta)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("events.clear", result.stderr)

    def test_fails_when_metadata_has_unknown_method(self) -> None:
        meta = json.loads(json.dumps(META))
        meta["methods"].append({"method": "world.missing", "category": "block", "purpose": "x"})
        result, _ = run(meta)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("world.missing", result.stderr)

    def test_fails_on_unknown_category(self) -> None:
        meta = json.loads(json.dumps(META))
        meta["methods"][0]["category"] = "nope"
        result, _ = run(meta)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nope", result.stderr)

    def test_excluded_reason_is_dropped_and_must_exist(self) -> None:
        meta = json.loads(json.dumps(META))
        meta["excluded_reasons"] = [{"reason": "zero_direction", "why": "x"}]
        result, out = run(meta)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads((out / "api.json").read_text(encoding="utf-8"))
        self.assertNotIn("zero_direction", [e["reason"] for e in data["errors"]])
        meta["excluded_reasons"] = [{"reason": "no_such_reason", "why": "x"}]
        result, _ = run(meta)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no_such_reason", result.stderr)

    def test_check_mode_detects_stale_output(self) -> None:
        result, out = run(META)
        self.assertEqual(result.returncode, 0, result.stderr)
        (out / "api.json").write_text("{}", encoding="utf-8")
        directory = out.parent
        check = subprocess.run(
            [sys.executable, str(BUILDER), "--wire", str(directory / "wire.md"), "--metadata", str(directory / "meta.json"), "--out", str(out), "--check"],
            cwd=ROOT, check=False, capture_output=True, text=True,
        )
        self.assertNotEqual(check.returncode, 0)

    def test_default_inputs_build_cleanly(self) -> None:
        result = subprocess.run([sys.executable, str(BUILDER), "--check"], cwd=ROOT, check=False, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
