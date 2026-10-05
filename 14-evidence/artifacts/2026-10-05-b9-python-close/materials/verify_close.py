"""Compare fixed knowledge bytes and inventory only the seven close targets.

Input: unmodified GitHub Contents API JSON captured at the contract commit.
No network access, server connections, credential reads, or source changes.
"""

import argparse
import base64
import hashlib
import json
from pathlib import Path

KNOWLEDGE_COMMIT = "099c40b0c312694712653885200f3114ea4bed33"
TARGETS = {
    "2026-10-04-b9-python-confirmation": "③",
    "2026-10-05-b9-python-work": "②",
    "2026-10-05-b9-python-tooling": "②",
    "2026-10-05-b9-python-release": "①",
    "2026-10-05-b9-python-live": "③",
    "2026-10-05-b9-dev-hello": "③",
    "2026-10-05-python-windows-entry": "③",
}
TRANSFERS = {
    "2026-10-05-b9-python-live": (
        "14-evidence/artifacts/2026-10-05-b9-dev-live/python/segment-2", False
    ),
    "2026-10-05-b9-dev-hello": (
        "14-evidence/artifacts/2026-10-05-b9-dev-live/python/saved-token-check", False
    ),
    "2026-10-05-python-windows-entry": (
        "14-evidence/artifacts/2026-10-05-python-windows-entry", True
    ),
}


def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_bytes())
    assert inputs["knowledge_commit"] == KNOWLEDGE_COMMIT
    listing = inputs["listings"]
    remote = {f["path"]: f for f in inputs["files"]}
    assert len(remote) == len(inputs["files"]) == 12
    assert {x["path"] for x in listing if x["type"] == "file"} == set(remote)
    assert all(x["type"] in ("file", "dir") for x in listing)
    inventory = []
    comparisons = []
    directory_sets = []
    for name, category in TARGETS.items():
        root = args.repo / "handoff-materials" / name
        paths = sorted(p for p in root.rglob("*") if p.is_file())
        assert paths and all(not p.is_symlink() for p in paths)
        entries = []
        for path in paths:
            data = path.read_bytes()
            entries.append({"path": path.relative_to(root).as_posix(), **identity(data)})
        inventory.append({
            "directory": name, "category": category,
            "file_count": len(entries), "bytes": sum(x["bytes"] for x in entries),
            "files": entries,
        })
        if name not in TRANSFERS:
            continue
        destination, flattened = TRANSFERS[name]
        selected = [p for p in paths if not flattened or p.parent == root / "materials"]
        expected = {
            destination + "/" + (p.name if flattened else p.relative_to(root).as_posix()): p
            for p in selected
        }
        actual = {p for p in remote if p.startswith(destination + "/")}
        assert set(expected) == actual, name
        directory_sets.append({
            "directory": name, "knowledge_destination": destination,
            "file_set_match": True, "file_count": len(expected),
            "local_not_transferred": [
                p.relative_to(root).as_posix() for p in paths if p not in selected
            ],
        })
        for destination_path, local_path in sorted(expected.items()):
            source = remote[destination_path]
            remote_data = base64.b64decode(source["content"])
            assert len(remote_data) == source["size"]
            assert hashlib.sha1(
                b"blob " + str(len(remote_data)).encode() + b"\0" + remote_data
            ).hexdigest() == source["sha"]
            local_data = local_path.read_bytes()
            equal = local_data == remote_data
            comparisons.append({
                "local_path": local_path.relative_to(args.repo).as_posix(),
                "knowledge_path": destination_path,
                "local": identity(local_data), "knowledge": identity(remote_data),
                "full_bytes_equal": equal,
            })
            assert equal, destination_path
    assert sum(x["file_count"] for x in inventory) == 45
    assert sum(x["bytes"] for x in inventory) == 150870
    result = {
        "knowledge_contract_commit": KNOWLEDGE_COMMIT,
        "inputs_identity": identity(args.inputs.read_bytes()),
        "result": "PASS", "transferred_file_count": len(comparisons),
        "transferred_bytes": sum(x["local"]["bytes"] for x in comparisons),
        "directory_sets": directory_sets, "comparisons": comparisons,
        "inventory": inventory,
        "mutations": {"target_directories": False, "deletions": False},
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "result": result["result"], "matched_files": len(comparisons),
        "matched_bytes": result["transferred_bytes"],
        "inventoried_files": 45, "inventoried_bytes": 150870,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
