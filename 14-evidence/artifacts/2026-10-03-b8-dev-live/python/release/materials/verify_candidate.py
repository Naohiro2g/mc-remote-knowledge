"""Verify newly built CI files against the approved B8 exact set."""

from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile


base = Path(__file__).resolve().parent
state_path = base / "state.json"
state = json.loads(state_path.read_text())
archive_path = base / "ci-37113256520.zip"
archive_bytes = archive_path.read_bytes()
assert len(archive_bytes) == 381099
assert hashlib.sha256(archive_bytes).hexdigest() == "a42db0b07080631daa201f74579c1940131df1ab9ca09e6c65a8a60efbce30d5"
out = base / "ci-37113256520"
out.mkdir(exist_ok=True)

with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert len(names) == 3 and "manifest.json" in names
    assert all(not PurePosixPath(name).is_absolute() and ".." not in PurePosixPath(name).parts for name in names)
    manifest = json.loads(archive.read("manifest.json"))
    assert manifest["schema"] == "mc-remote.release-manifest" and manifest["schema_version"] == 1
    assert manifest["source_commit"] == state["candidate_commit"]
    assert manifest["release_tag"] is None
    assert manifest["bundled_wirescope_source_commit"] == "df34849d2502a498a06c5fe07a91d03e925124eb"
    verified = []
    for item in manifest["artifacts"]:
        role = item["role"]
        assert role in state["expected"] and item["kind"] == "https-file"
        matches = [name for name in names if PurePosixPath(name).name == item["file"]]
        assert len(matches) == 1
        data = archive.read(matches[0])
        actual = {
            "role": role,
            "file": item["file"],
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
        verified.append(actual)
        print(json.dumps(actual, ensure_ascii=False))
        assert actual["sha256"] == item["sha256"], "CI bytes do not match CI manifest"
    assert len(verified) == 2 and {item["role"] for item in verified} == {"wheel", "sdist"}
    frozen_match = all(
        item["bytes"] == state["expected"][item["role"]]["bytes"]
        and item["sha256"] == state["expected"][item["role"]]["sha256"]
        for item in verified
    )
    state["ci_artifact_id"] = 11271101046
    state["ci_artifacts"] = verified
    state["artifact_verification"] = "PASS" if frozen_match else "FAIL"
    state["phase"] = (
        "CI artifacts matched frozen wheel and sdist; release publication pending"
        if frozen_match
        else "STOP: CI artifacts differ from frozen identity; release prohibited"
    )
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    for name in names:
        path = out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(archive.read(name))
    print("CI manifest SHA-256:", hashlib.sha256(archive.read("manifest.json")).hexdigest())
    if not frozen_match:
        raise SystemExit("STOP: frozen artifact mismatch; do not publish")

print("PASS: new tag-target CI artifacts exactly match both frozen files")
