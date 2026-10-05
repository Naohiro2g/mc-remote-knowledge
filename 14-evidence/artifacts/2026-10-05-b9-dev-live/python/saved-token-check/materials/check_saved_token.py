"""Read-only hello smoke with the frozen wheel; never print credentials."""

import argparse
import ast
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import subprocess
import sys

from mc_remote import Minecraft
from mc_remote.auth import _token_file, load_token
from mc_remote.connection import Connection, McRpcError


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--wheel", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = {
        "test_class": "live-auto",
        "scope": "saved-token authenticated hello only",
        "knowledge_contract_commit": "561de98b5c15864ac9b86cb6dcaeef1f20ce635b",
        "knowledge_contract_path": "00-hub/b9-gate-live-test-sheet_ja.md",
        "exact_set": "b9-integrated-artifact-set-1",
        "python_source_commit": "b901c88fe41b67530ff353271683ece9fd453076",
        "wheel_bytes": args.wheel.stat().st_size,
        "wheel_sha256": hashlib.sha256(args.wheel.read_bytes()).hexdigest(),
        "installed_version": version("minecraft-remote-api"),
        "endpoint_profile": "normal-dev",
        "pairing_performed": False,
        "token_emitted": False,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "NOT_RUN",
    }
    connection = None
    before = None
    token_path = Path(_token_file())
    try:
        assert report["wheel_bytes"] == 196221
        assert report["wheel_sha256"] == "e166bc9c14c425b3859f9af6c7af52900b58d1769fc077a3524a5368d05638c6"
        assert report["installed_version"] == "2320.0.0b9"
        assert "site-packages" in str(Path(sys.modules["mc_remote"].__file__).resolve())
        values = {}
        for node in ast.parse(args.profile.read_text()).body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        try:
                            values[target.id] = ast.literal_eval(node.value)
                        except (ValueError, TypeError):
                            pass
        host, port = values["ADRS_MCR"], values["PORT_MCR"]
        ssh = subprocess.run(["ssh", "-G", "m720s2"], capture_output=True, text=True, check=True)
        expected_host = next(line.split(" ", 1)[1] for line in ssh.stdout.splitlines() if line.startswith("hostname "))
        assert host == expected_host and port == 25575
        report["endpoint_matches_authorized_alias"] = True
        before = token_path.read_bytes() if token_path.exists() else None
        token = load_token(f"{host}:{port}")
        report["stored_token_present"] = bool(token)
        if not token:
            report.update(status="FAIL", stage="local-token", reason="stored_token_missing")
            return 1
        report["stage"] = "tcp-connect"
        connection = Connection(host, port, debug=False)
        connection.request_timeout = 15.0
        report["tcp_connected"] = True
        report["stage"] = "authenticated-hello"
        mc = Minecraft(connection)
        result = mc.hello(token)
        allowed = (
            "protocol", "mc_version", "supported_mc_versions", "dimension",
            "origin", "world_constants", "permissions", "catalogHash", "catalog_hash",
        )
        report["hello_request"] = {"method": "hello", "params": {"protocol": "23.2.0", "auth": {"token": "[REDACTED]"}}}
        report["hello_result"] = {key: result[key] for key in allowed if key in result}
        report["protocol_matches"] = result.get("protocol") == "23.2.0"
        report["mc_version_matches"] = result.get("mc_version") == "1.21.11"
        report["saved_token_accepted"] = True
        report["status"] = "PASS" if report["protocol_matches"] and report["mc_version_matches"] else "FAIL"
        if report["status"] != "PASS":
            report["reason"] = "hello_identity_mismatch"
        return 0 if report["status"] == "PASS" else 1
    except Exception as exc:
        report.update(status="FAIL", exception_type=type(exc).__name__)
        if isinstance(exc, McRpcError):
            report["code"] = exc.code
            reason = exc.reason
            report["reason"] = reason if isinstance(reason, str) and re.fullmatch(r"[a-z_]{1,64}", reason) else "unrecognized_reason_redacted"
        return 1
    finally:
        if connection is not None:
            try:
                connection.close()
                report["close"] = "PASS"
            except Exception as exc:
                report["close"] = type(exc).__name__
        after = token_path.read_bytes() if token_path.exists() else None
        if before is not None:
            report["token_store_unchanged"] = before == after
        report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
