"""Two-phase credential continuity diagnostic; use the frozen CI wheel."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys

from mc_remote.auth import config_dir, load_token, pair, save_token
from mc_remote.connection import Connection, McRpcError
from mc_remote.minecraft import PROTOCOL


ROOT = Path(__file__).resolve().parents[3]
WHEEL = ROOT / "handoff-materials/2026-10-01-b8-python-successor/materials/ci-36860299749/minecraft_remote_api-2320.0.0b8-py3-none-any.whl"
WHEEL_SHA = "dcedff010feac0d5df24ff85dd84b321fb819f78563c39431ac32d9d75bc0180"
STATE_NAME = "b8-dev-token-upgrade-2026-10-03.json"


class DiagnosticStop(Exception):
    pass


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def read_endpoint(path):
    values = {}
    for node in ast.parse(path.read_text()).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in {"ADRS_MCR", "PORT_MCR"}:
                values[target.id] = ast.literal_eval(node.value)
    host, port = values.get("ADRS_MCR"), values.get("PORT_MCR")
    if not isinstance(host, str) or not host or type(port) is not int or not 1 <= port <= 65535:
        raise DiagnosticStop("endpoint configuration missing or invalid")
    return host, port


def save_private_state(path, state):
    temporary = path.with_suffix(".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(state, stream)
    os.chmod(temporary, 0o600)
    temporary.replace(path)


def open_connection(host, port):
    connection = Connection(host, port)
    connection.request_timeout = 10
    connection.socket.settimeout(10)
    return connection


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=["b7", "b8"], required=True)
    parser.add_argument("--config", type=Path, required=True, help="Existing local param_mc_remote.py; endpoint values are never printed")
    args = parser.parse_args()
    protocol = "23.1.0" if args.phase == "b7" else "23.2.0"
    summary = {
        "knowledge_commit": "749ba60dc8c18938e50ce66b8e820aac4401c69e",
        "exact_set": "b8-integrated-artifact-set-1",
        "client_commit": "52d35f5304e62f465c1f47ab47c00fe9bcf62470",
        "wheel_sha256": WHEEL_SHA,
        "phase": args.phase,
        "test_class": "live-human" if args.phase == "b7" else "live-auto",
        "expected_protocol": protocol,
        "status": "FAIL",
        "mc_version": None,
        "pairing_started": False,
        "world_write_calls": 0,
        "hello_request": None,
    }
    conn = None
    stage = "artifact preflight"
    try:
        if hashlib.sha256(WHEEL.read_bytes()).hexdigest() != WHEEL_SHA:
            raise DiagnosticStop("frozen wheel digest mismatch")
        if importlib.metadata.version("minecraft-remote-api") != "2320.0.0b8" or PROTOCOL != "23.2.0":
            raise DiagnosticStop("frozen B8 wheel environment required")
        stage = "endpoint configuration"
        host, port = read_endpoint(args.config)
        key = f"b8-gate-upgrade-dev-2026-10-03:{host}:{port}"
        endpoint_digest = digest(f"{host}:{port}")
        state_path = Path(config_dir()) / STATE_NAME

        if args.phase == "b7":
            if state_path.exists() or load_token(key):
                raise DiagnosticStop("existing continuity state; do not start a second pairing")
            stage = "b7 unauthenticated preflight"
            conn = open_connection(host, port)
            summary["preflight_request"] = {"method": "hello", "params": {"protocol": protocol}}
            try:
                conn.rpc("hello", {"protocol": protocol})
            except McRpcError as error:
                if error.reason != "auth_required":
                    raise
                summary["unauthenticated_hello_reason"] = error.reason
            else:
                raise DiagnosticStop("expected auth_required; authentication enforcement must stay ON")
            conn.close()
            conn = open_connection(host, port)
            stage = "b7 new session pairing"
            summary["pairing_started"] = True
            token = pair(conn, token_type="session")
            stage = "save b7 token"
            save_token(key, token)
            state = {"token_key": key, "endpoint_digest": endpoint_digest, "token_digest": digest(token), "phase": "b7_token_saved"}
            save_private_state(state_path, state)
            summary["token_saved"] = True
            conn.close()
            conn = None
        else:
            stage = "load same saved b7 token"
            if not state_path.is_file():
                raise DiagnosticStop("b7 verification state missing")
            state = json.loads(state_path.read_text())
            if state.get("phase") != "b7_verified" or state.get("endpoint_digest") != endpoint_digest or state.get("token_key") != key:
                raise DiagnosticStop("verified b7 state or endpoint mismatch")

        token = load_token(key)
        if not token or digest(token) != state["token_digest"]:
            raise DiagnosticStop("saved token missing or changed; pairing will not be retried")
        summary["same_saved_token"] = True
        stage = f"{args.phase} authenticated hello"
        conn = open_connection(host, port)
        summary["hello_request"] = {"method": "hello", "params": {"protocol": protocol, "auth": {"token": "[REDACTED]"}}}
        hello = conn.rpc("hello", {"protocol": protocol, "auth": {"token": token}})
        if not isinstance(hello, dict):
            raise DiagnosticStop("hello result is not an object")
        summary["hello_response"] = {"protocol": hello.get("protocol"), "mc_version": hello.get("mc_version")}
        summary["mc_version"] = hello.get("mc_version")
        if hello.get("protocol") != protocol or hello.get("mc_version") != "1.21.11":
            raise DiagnosticStop("hello version mismatch; stop this segment")
        if args.phase == "b7":
            state["phase"] = "b7_verified"
            save_private_state(state_path, state)
        summary["status"] = "PASS"
    except McRpcError as error:
        summary["failure"] = {"stage": stage, "code": error.code, "reason": error.reason}
    except DiagnosticStop as error:
        summary["failure"] = {"stage": stage, "reason": str(error)}
    except Exception as error:
        # Exception text can contain private endpoints or credential paths.
        summary["failure"] = {"stage": stage, "type": type(error).__name__}
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as error:
                summary["close_failure_type"] = type(error).__name__
                summary["status"] = "FAIL"
        output = Path(__file__).parent / f"{args.phase}_summary.json"
        output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
