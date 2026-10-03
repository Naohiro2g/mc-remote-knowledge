#!/usr/bin/env python3
"""Run the frozen live-auto runner and save a sanitized RPC transcript."""

import hashlib
import importlib.util
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


RUNNER_SHA256 = "7a093d27ac349023e7be90c48597ead1a1207772a4fee084933ee2f8c794352f"
SOURCE_COMMIT = "17309919f6340b07abbbe16476ad1d4f762518c0"
KNOWLEDGE_COMMIT = "749ba60dc8c18938e50ce66b8e820aac4401c69e"
SENSITIVE_KEYS = {"token", "pairing_id", "player", "player_uuid", "uuid", "credential_id", "domain_id"}
TOKEN_PATTERN = re.compile(r"\bmcr[slp]_[A-Za-z0-9_-]+\b")
UUID_PATTERN = re.compile(r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b")


class Redactor:
    def __init__(self, host):
        self.secrets = {host} if host else set()

    def learn(self, value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in SENSITIVE_KEYS and isinstance(child, str) and child:
                    self.secrets.add(child)
                self.learn(child)
        elif isinstance(value, list):
            for child in value:
                self.learn(child)

    def string(self, value):
        value = TOKEN_PATTERN.sub("[REDACTED_TOKEN]", value)
        value = UUID_PATTERN.sub("[REDACTED_UUID]", value)
        for secret in sorted(self.secrets, key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]")
        return value

    def clean(self, value):
        self.learn(value)
        if isinstance(value, dict):
            return {key: "[REDACTED]" if key in SENSITIVE_KEYS else self.clean(child)
                    for key, child in value.items()}
        if isinstance(value, list):
            return [self.clean(child) for child in value]
        if isinstance(value, str):
            return self.string(value)
        return value


class SafeTee:
    def __init__(self, stream, log, redactor):
        self.stream, self.log, self.redactor = stream, log, redactor

    def write(self, value):
        safe = self.redactor.string(value)
        self.log.write(safe)
        self.log.flush()
        self.stream.write(safe)
        self.stream.flush()
        return len(value)

    def flush(self):
        self.log.flush()
        self.stream.flush()

    def isatty(self):
        return self.stream.isatty()


def main():
    materials = Path(__file__).resolve().parent
    runner_path = materials.parents[2] / "scripts" / "live_auto.py"
    if hashlib.sha256(runner_path.read_bytes()).hexdigest() != RUNNER_SHA256:
        raise SystemExit("Frozen live-auto runner digest mismatch; no connection attempted")
    transcript_path = materials / "rpc-transcript.jsonl"
    log_path = materials / "live-auto.log"
    if transcript_path.exists() or log_path.exists():
        raise SystemExit("Existing evidence must be preserved; no connection attempted")
    host = "127.0.0.1"
    for index, argument in enumerate(sys.argv[1:], 1):
        if argument == "--host" and index + 1 < len(sys.argv):
            host = sys.argv[index + 1]
        elif argument.startswith("--host="):
            host = argument.split("=", 1)[1]
    redactor = Redactor(host)
    spec = importlib.util.spec_from_file_location("frozen_live_auto", runner_path)
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    original_stdout, original_stderr = sys.stdout, sys.stderr
    with transcript_path.open("x", encoding="utf-8") as transcript, log_path.open("x", encoding="utf-8") as log:
        def record(kind, **details):
            entry = {"time_utc": datetime.now(timezone.utc).isoformat(), "kind": kind, **details}
            transcript.write(json.dumps(redactor.clean(entry), ensure_ascii=False, separators=(",", ":")) + "\n")
            transcript.flush()

        original_init, original_call, original_notify = runner.Rpc.__init__, runner.Rpc.call, runner.Rpc.notify
        epoch_count = 0

        def rpc_init(self, *args, **kwargs):
            nonlocal epoch_count
            epoch_count += 1
            self.evidence_epoch = epoch_count
            original_init(self, *args, **kwargs)

        def rpc_call(self, method, params):
            record("send", epoch=self.evidence_epoch, request={"jsonrpc": "2.0", "id": self._next_id + 1,
                                                             "method": method, "params": params})
            try:
                response = original_call(self, method, params)
            except BaseException as error:
                record("rpc_failure", epoch=self.evidence_epoch, method=method,
                       error_type=type(error).__name__, error=str(error))
                raise
            record("receive", epoch=self.evidence_epoch, method=method, response=response)
            return response

        def rpc_notify(self, method, params):
            record("send", epoch=self.evidence_epoch, request={"jsonrpc": "2.0", "method": method, "params": params})
            return original_notify(self, method, params)

        runner.Rpc.__init__, runner.Rpc.call, runner.Rpc.notify = rpc_init, rpc_call, rpc_notify
        sys.stdout, sys.stderr = SafeTee(original_stdout, log, redactor), SafeTee(original_stderr, log, redactor)
        record("identity", exact_set="b8-integrated-artifact-set-1", knowledge_commit=KNOWLEDGE_COMMIT,
               source_commit=SOURCE_COMMIT, runner_sha256=RUNNER_SHA256)
        try:
            code = runner.main()
            record("completion", exit_code=code)
            return code
        finally:
            sys.stdout, sys.stderr = original_stdout, original_stderr


if __name__ == "__main__":
    sys.exit(main())
