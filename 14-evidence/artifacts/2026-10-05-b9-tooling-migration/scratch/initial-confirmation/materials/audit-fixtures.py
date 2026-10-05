import hashlib
import json
from pathlib import Path
import subprocess

baseline_commit = "691576f60b7f0824e1753bd6823901d01fbe2422"
inventory = Path(__file__).with_name("b8-fixtures-baseline.json")
rows = json.loads(inventory.read_text())
assert len(rows) == 12
for row in rows:
    current = Path(row["path"]).read_bytes()
    frozen = subprocess.check_output(["git", "show", baseline_commit + ":" + row["path"]])
    assert current == frozen, row["path"]
    assert len(current) == row["bytes"], row["path"]
    assert hashlib.sha256(current).hexdigest() == row["sha256"], row["path"]
print(json.dumps({
    "result": "PASS",
    "baseline_commit": baseline_commit,
    "fixtures_verified": len(rows),
    "comparison": "working files == published b8 source == knowledge inventory bytes/SHA-256",
}, ensure_ascii=False, indent=2))
