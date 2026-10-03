"""B8 segment 2 remainder, derived from the approved corrected runner."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import runpy
import sys
import time

from mc_remote import Minecraft
from mc_remote.auth import config_dir, load_token
from mc_remote.connection import McRpcError


FOLDER = Path(__file__).resolve().parent
BASE = FOLDER.parent
APPROVED_RUNNER_SHA = "15c5c2cfa1ace74b03fd21c54d0ac575b656f75a39315754f283d8255fbf1003"
SAMPLE_SHA = "e3824c3800aea4acc3ca1141a289e5a04d34c52cb2492af25b38f050bfe824d3"
helpers = runpy.run_path(str(BASE / "python_representative.py"))
DiagnosticStop = helpers["DiagnosticStop"]
STATE_NAME = helpers["STATE_NAME"]
WHEEL = helpers["WHEEL"]
WHEEL_SHA = helpers["WHEEL_SHA"]
digest = helpers["digest"]
read_endpoint = helpers["read_endpoint"]


def main():
    summary = {
        "knowledge_commit": "396326def73d99aae91dca4de9416f4eca6d2aea",
        "exact_set": "b8-integrated-artifact-set-1",
        "client_commit": "52d35f5304e62f465c1f47ab47c00fe9bcf62470",
        "wheel_sha256": WHEEL_SHA,
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derived_from_runner_sha256": APPROVED_RUNNER_SHA,
        "sample_sha256": SAMPLE_SHA,
        "test_class": "live-auto with live-human WireScope observation",
        "reused_pass": ["short import", "entity lifecycle", "ParticleSpec", "playSound", "run-1 WireScope frames"],
        "status": "FAIL",
        "pairing_started": False,
        "results": [],
        "human_observations": {},
        "temporary_block_remaining": False,
        "non_claim": ["actual server SoundGroup volume/pitch numbers", "2-player receiver difference", "rendering", "audibility", "localization"],
    }
    stage = "artifact preflight"
    mc = None
    frame_file = None
    frames = []

    def passed(name, **facts):
        summary["results"].append({"operation": name, "status": "PASS", **facts})
        print("PASS " + name, flush=True)

    def checkpoint(name, command):
        print(f"CHECKPOINT {name}: waiting for {command}", flush=True)
        if input().strip() != command:
            raise DiagnosticStop("human checkpoint not confirmed")
        summary["human_observations"][name] = "human owner confirmed"

    def sound_call(kind, control, kwargs, expected_options):
        before = len(frames)
        mc.playBlockSound(3, 1, 0, kind, **kwargs)
        sends = [f for f in frames[before:] if f["method"] == "world.playBlockSound" and f["direction"] == "send"]
        if len(sends) != 1:
            raise DiagnosticStop("exactly one playBlockSound request expected")
        expected = [3, 1, 0, kind]
        if expected_options is not None:
            expected.append(expected_options)
        if sends[0]["payload"]["params"] != expected:
            raise DiagnosticStop("playBlockSound wire options differ from expected controls")
        receives = [f for f in frames[before:] if f["direction"] == "receive" and f["request_id"] == sends[0]["request_id"]]
        if len(receives) != 1 or receives[0]["payload"] != {"result": None}:
            raise DiagnosticStop("playBlockSound result:null expected")
        passed(f"playBlockSound {kind} {control}", wire_params=expected, result=None)
        time.sleep(0.25)

    try:
        if hashlib.sha256((BASE / "python_representative.py").read_bytes()).hexdigest() != APPROVED_RUNNER_SHA:
            raise DiagnosticStop("approved base runner digest mismatch")
        if hashlib.sha256(WHEEL.read_bytes()).hexdigest() != WHEEL_SHA or importlib.metadata.version("minecraft-remote-api") != "2320.0.0b8":
            raise DiagnosticStop("frozen wheel identity mismatch")
        sample = BASE / "particle_graph_frozen.py"
        if hashlib.sha256(sample.read_bytes()).hexdigest() != SAMPLE_SHA:
            raise DiagnosticStop("frozen graph sample digest mismatch")
        if (FOLDER / "summary.json").exists() or (FOLDER / "frames.jsonl").exists():
            raise DiagnosticStop("run-2 evidence already exists; refusing overwrite")
        host, port = read_endpoint(BASE / "param_dev.py")
        state = json.loads((Path(config_dir()) / STATE_NAME).read_text())
        if state.get("endpoint_digest") != digest(f"{host}:{port}"):
            raise DiagnosticStop("continuity endpoint mismatch")
        token = load_token(state["token_key"])
        if not token or digest(token) != state["token_digest"]:
            raise DiagnosticStop("same saved token unavailable")
        for name in ("MCREMOTE_API_HOST", "JRP_API_HOST", "MCREMOTE_API_PORT", "JRP_API_PORT"):
            os.environ.pop(name, None)
        stage = "WireScope startup"
        mc = Minecraft.create(address=host, port=port, handshake=False, pair=False, sync_catalog=False, wirescope=True)
        runtime = mc._wirescope_runtime
        if runtime is None or mc._observer is None:
            raise DiagnosticStop("WireScope station did not start")
        frame_file = (FOLDER / "frames.jsonl").open("x")

        def capture(frame):
            # Product-sanitized frames; retain the unchanged station sink.
            frames.append(frame)
            frame_file.write(json.dumps(frame, ensure_ascii=False) + "\n")
            frame_file.flush()
            runtime.pipeline.accept_frame(frame)

        mc._observer.set_frame_consumer(capture)
        stage = "authenticated hello"
        mc.hello(token)
        summary["hello"] = {"protocol": mc.protocol, "mc_version": mc.mc_version}
        if mc.protocol != "23.2.0" or mc.mc_version != "1.21.11":
            raise DiagnosticStop("hello version mismatch; body skipped")
        passed("authenticated hello")
        print("WIRESCOPE_URL " + runtime.url, flush=True)
        checkpoint("WireScope attached and Minecraft logged in", "ready")

        stage = "build context at player feet"
        origin = tuple(mc._origin)
        player = mc.getPos()
        mc.setDimension(player["dimension"])
        mc.setBuildOrigin(*(math.floor(origin[i] + player["pos"][i]) for i in range(3)))

        stage = "getBlock original value"
        original = mc.getBlock(3, 1, 0)
        original_spec = {"block_id": original.block_id, "state": dict(original.state)}
        passed("getBlock original BlockValue", block=original_spec)
        if original.block_id in {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}:
            stage = "temporary stone"
            mc.setBlock(3, 1, 0, "stone")
            summary["temporary_block_remaining"] = True
            target = mc.getBlock(3, 1, 0)
            if target.block_id != "minecraft:stone" or dict(target.state) != {}:
                raise DiagnosticStop("temporary stone readback differs")
            passed("temporary stone readback", block={"block_id": target.block_id, "state": dict(target.state)})
        else:
            target = original
        summary["sound_target_block"] = {"block_id": target.block_id, "state": dict(target.state)}

        controls = [
            ("options omitted", {"receiver": None}, None),
            ("pitch override self", {"pitch": 0.75, "receiver": "self"}, {"pitch": 0.75, "receiver": "self"}),
            ("note override world", {"note": 18, "receiver": "world"}, {"note": 18, "receiver": "world"}),
        ]
        for kind in ("place", "hit", "break", "step", "fall"):
            for label, kwargs, expected_options in controls:
                stage = f"playBlockSound {kind} {label}"
                sound_call(kind, label, kwargs, expected_options)
        stage = "playBlockSound Python default call"
        sound_call("hit", "Python default call", {}, {"receiver": "world"})

        stage = "restore original block"
        if summary["temporary_block_remaining"]:
            mc.setBlock(3, 1, 0, original.block_id, state=original.state)
        restored = mc.getBlock(3, 1, 0)
        if restored.block_id != original.block_id or dict(restored.state) != dict(original.state):
            raise DiagnosticStop("restored BlockValue differs from original")
        summary["temporary_block_remaining"] = False
        passed("original block restored and read back", block={"block_id": restored.block_id, "state": dict(restored.state)})

        stage = "human core frame observation"
        checkpoint("getBlock payload and playBlockSound frames visible", "graph")
        stage = "frozen 3D graph sample"
        before = len(frames)
        runpy.run_path(str(sample))["draw_graph"](mc)
        sends = [f for f in frames[before:] if f["direction"] == "send" and f["method"] == "world.spawnParticle"]
        receives = [f for f in frames[before:] if f["direction"] == "receive" and f["method"] == "world.spawnParticle"]
        if len(sends) != 81 or len(receives) != 81 or any(f["payload"] != {"result": 1} for f in receives):
            raise DiagnosticStop("graph expected 81 successful single-particle roundtrips")
        passed("frozen 3D graph sample", particle_requests=81, particle_results=81)
        stage = "human graph frame observation"
        checkpoint("graph frames visible", "finish")
        summary["status"] = "PASS"
    except McRpcError as error:
        summary["failure"] = {"stage": stage, "code": error.code, "reason": error.reason}
    except DiagnosticStop as error:
        summary["failure"] = {"stage": stage, "reason": str(error)}
    except Exception as error:
        summary["failure"] = {"stage": stage, "type": type(error).__name__}
    finally:
        if mc is not None:
            try:
                mc.close()
            except Exception as error:
                summary["close_failure_type"] = type(error).__name__
                summary["status"] = "FAIL"
        if frame_file is not None:
            frame_file.close()
        summary["frame_count"] = len(frames)
        # On failure do not issue further world calls. Report any test block left.
        output = FOLDER / "summary.json"
        if not output.exists():
            output.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
