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
SOURCE_COMMIT = "5cb33ebad4bf2c5e36c3433b0f70fe6070915b00"
KNOWLEDGE_COMMIT = "561de98b5c15864ac9b86cb6dcaeef1f20ce635b"
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
        original_close = runner.Rpc.close
        original_structured = runner.verify_structured_blocks
        original_acquire = runner.acquire_interactive_token
        acquired = {}
        cleanup = {"spawned": 0, "removed_in_test": 0, "removed_after_test": 0,
                   "already_absent": 0, "blocks_saved": 0, "blocks_restored": 0, "failures": []}
        epoch_count = 0

        def rpc_init(self, *args, **kwargs):
            nonlocal epoch_count
            epoch_count += 1
            self.evidence_epoch = epoch_count
            self.evidence_spawned = set()
            self.evidence_blocks = {}
            self.evidence_closed = False
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
            if method == "world.spawnEntity" and "error" not in response:
                handle = response.get("result")
                if isinstance(handle, str) and runner.HANDLE.fullmatch(handle):
                    self.evidence_spawned.add(handle)
                    cleanup["spawned"] += 1
            if method == "entity.remove" and "error" not in response and params[0] in self.evidence_spawned:
                self.evidence_spawned.remove(params[0])
                cleanup["removed_in_test"] += 1
            return response

        def rpc_notify(self, method, params):
            record("send", epoch=self.evidence_epoch, request={"jsonrpc": "2.0", "method": method, "params": params})
            return original_notify(self, method, params)

        def structured_with_snapshot(rpc, height):
            # These are the nine locations written by the pinned runner, including notifications.
            coordinates = [(x, height + 1, 0) for x in range(5)]
            coordinates += [(3, height + 1, 1), (4, height + 1, 1),
                            (7, height + 1, 0), (8, height + 1, 0)]
            for coordinate in coordinates:
                rpc.evidence_blocks[coordinate] = runner.result(rpc.call("world.getBlock", list(coordinate)))
                cleanup["blocks_saved"] += 1
            record("block_snapshots", epoch=rpc.evidence_epoch,
                   blocks=[{"pos": list(pos), "value": value} for pos, value in rpc.evidence_blocks.items()])
            return original_structured(rpc, height)

        def rpc_close(self):
            if self.evidence_closed:
                return
            try:
                for handle in sorted(self.evidence_spawned):
                    response = self.call("entity.remove", [handle])
                    if "error" not in response:
                        runner.require_null_result("owned entity cleanup", response)
                        cleanup["removed_in_test"] -= 1
                        cleanup["removed_after_test"] += 1
                    elif runner.reason(response) == "entity_not_found":
                        cleanup["already_absent"] += 1
                    else:
                        raise AssertionError(f"owned entity cleanup: {response}")
                for coordinate, value in self.evidence_blocks.items():
                    runner.require_null_result("block restoration", self.call("world.setBlock", [*coordinate, value]))
                    restored = runner.result(self.call("world.getBlock", list(coordinate)))
                    if restored != value:
                        raise AssertionError(f"block restoration mismatch at {coordinate}: {restored}")
                    cleanup["blocks_restored"] += 1
            except BaseException as error:
                cleanup["failures"].append(redactor.string(str(error)))
                record("cleanup_failure", epoch=self.evidence_epoch, error=str(error))
                print(f"FAIL cleanup: {error}", file=sys.stderr)
            finally:
                self.evidence_closed = True
                original_close(self)

        def acquire_and_keep_in_memory(args, **kwargs):
            token = original_acquire(args, **kwargs)
            acquired.update(args=args, token=token)
            return token

        runner.Rpc.__init__, runner.Rpc.call, runner.Rpc.notify = rpc_init, rpc_call, rpc_notify
        runner.Rpc.close = rpc_close
        runner.verify_structured_blocks = structured_with_snapshot
        runner.acquire_interactive_token = acquire_and_keep_in_memory
        sys.stdout, sys.stderr = SafeTee(original_stdout, log, redactor), SafeTee(original_stderr, log, redactor)
        record("identity", exact_set="b9-integrated-artifact-set-1", knowledge_commit=KNOWLEDGE_COMMIT,
               source_commit=SOURCE_COMMIT, runner_sha256=RUNNER_SHA256)
        try:
            code = runner.main()
            if cleanup["failures"]:
                code = 1
            if code == 0:
                try:
                    rpc = runner.connect(acquired["args"], acquired["token"])
                    try:
                        response = rpc.call("chat.post", ["McRemote b9 live-auto: chat.post result null verification"])
                        runner.require_null_result("chat.post", response)
                        print("PASS chat.post: id response has exact result:null")
                        record("chat_null_confirmation", response=response)
                    finally:
                        rpc.close()
                except (AssertionError, OSError, RuntimeError, KeyError) as error:
                    record("chat_null_failure", error=str(error))
                    print(f"FAIL chat.post: {error}", file=sys.stderr)
                    code = 1
            record("cleanup_summary", **cleanup)
            (materials / "cleanup-summary.json").write_text(
                json.dumps(cleanup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            record("completion", exit_code=code)
            return code
        finally:
            sys.stdout, sys.stderr = original_stdout, original_stderr


if __name__ == "__main__":
    sys.exit(main())
