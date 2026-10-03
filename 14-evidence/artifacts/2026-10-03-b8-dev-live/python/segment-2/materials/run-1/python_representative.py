"""Frozen-wheel B8 representative calls with a human WireScope observer."""

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

helpers = runpy.run_path(str(Path(__file__).with_name("token_upgrade.py")))
DiagnosticStop = helpers["DiagnosticStop"]
STATE_NAME = helpers["STATE_NAME"]
WHEEL = helpers["WHEEL"]
WHEEL_SHA = helpers["WHEEL_SHA"]
digest = helpers["digest"]
read_endpoint = helpers["read_endpoint"]


FOLDER = Path(__file__).resolve().parent


def main():
    summary = {
        "knowledge_commit": "749ba60dc8c18938e50ce66b8e820aac4401c69e",
        "exact_set": "b8-integrated-artifact-set-1",
        "client_commit": "52d35f5304e62f465c1f47ab47c00fe9bcf62470",
        "wheel_sha256": WHEEL_SHA,
        "test_class": "live-auto with live-human WireScope observation",
        "status": "FAIL",
        "pairing_started": False,
        "results": [],
        "human_observations": {},
        "created_entity_remaining": False,
        "temporary_block_remaining": False,
    }
    mc = None
    stage = "artifact preflight"
    frames = []
    frame_file = None

    def passed(name, **facts):
        summary["results"].append({"operation": name, "status": "PASS", **facts})
        print(f"PASS {name}", flush=True)

    def checkpoint(name, expected):
        print(f"CHECKPOINT {name}: waiting for {expected}", flush=True)
        command = input().strip()
        if command != expected:
            raise DiagnosticStop("human checkpoint not confirmed; stop")
        summary["human_observations"][name] = "human owner confirmed"

    try:
        if hashlib.sha256(WHEEL.read_bytes()).hexdigest() != WHEEL_SHA or importlib.metadata.version("minecraft-remote-api") != "2320.0.0b8":
            raise DiagnosticStop("frozen wheel identity mismatch")
        host, port = read_endpoint(FOLDER / "param_dev.py")
        state = json.loads((Path(config_dir()) / STATE_NAME).read_text())
        if state.get("endpoint_digest") != digest(f"{host}:{port}"):
            raise DiagnosticStop("continuity endpoint mismatch")
        token = load_token(state["token_key"])
        if not token or digest(token) != state["token_digest"]:
            raise DiagnosticStop("same saved token unavailable")
        for name in ("MCREMOTE_API_HOST", "JRP_API_HOST", "MCREMOTE_API_PORT", "JRP_API_PORT"):
            os.environ.pop(name, None)
        stage = "WireScope startup"
        # handshake=False avoids automatic pairing or credential deletion.
        mc = Minecraft.create(address=host, port=port, handshake=False, pair=False, sync_catalog=False, wirescope=True)
        runtime = mc._wirescope_runtime
        if runtime is None or mc._observer is None:
            raise DiagnosticStop("WireScope station did not start")
        frame_file = (FOLDER / "representative_frames.jsonl").open("w")

        def capture(frame):
            # The product observer has already removed auth, player UUIDs,
            # pairing IDs and endpoints. Preserve the normal station sink.
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
        passed("short import and authenticated hello")
        print("WIRESCOPE_URL " + runtime.url, flush=True)
        checkpoint("WireScope attached and Minecraft logged in", "ready")

        stage = "build context at player feet"
        initial_origin = tuple(mc._origin)
        player = mc.getPos()
        foot = [math.floor(initial_origin[i] + player["pos"][i]) for i in range(3)]
        mc.setDimension(player["dimension"])
        mc.setBuildOrigin(*foot)
        passed("build context at player feet")

        stage = "spawn cow with bare resource ID"
        handle = mc.spawnEntity(2, 1, 2, "cow")
        summary["created_entity_remaining"] = True
        passed("spawnEntity bare cow")
        stage = "nearby includes spawned cow"
        nearby = mc.getNearbyEntities(2, 1, 2, radius=3, max_entities=16)
        if not any(entity.handle == handle and entity.type == "minecraft:cow" for entity in nearby):
            raise DiagnosticStop("spawned cow missing from nearby snapshot")
        passed("getNearbyEntities", entity_count=len(nearby), spawned_handle_present=True)
        stage = "entity pose get"
        pose = mc.getEntityPose(handle)
        passed("getEntityPose", dimension=pose["dimension"])
        stage = "entity pose set"
        x, y, z = pose["pos"]
        moved = mc.setEntityPose(handle, pose["dimension"], x + 0.5, y + 0.5, z, 45, 0)
        if moved["dimension"] != pose["dimension"]:
            raise DiagnosticStop("entity setPose dimension changed unexpectedly")
        passed("setEntityPose", post_read_pose=moved)
        stage = "entity remove"
        mc.removeEntity(handle)
        summary["created_entity_remaining"] = False
        passed("removeEntity")

        for receiver in ("world", "self"):
            stage = f"dust ParticleSpec {receiver}"
            dust = {"particle_id": "dust", "receiver": receiver, "data": {"color": [64, 160, 255], "size": 1.0}}
            count = mc.spawnParticle(0, 2, 2, 0.2, 0.2, 0.2, dust, 0, 8)
            passed(stage, result=count)
            stage = f"block ParticleSpec {receiver}"
            block = {"particle_id": "block", "receiver": receiver, "data": {"block_id": "stone", "state": {}}}
            count = mc.spawnParticle(1, 2, 2, 0.2, 0.2, 0.2, block, 0, 8)
            passed(stage, result=count)
            time.sleep(0.25)
        stage = "bare flame"
        count = mc.spawnParticle(2, 2, 2, 0, 0, 0, "flame", 0, 4)
        passed("spawnParticle bare flame", result=count)

        stage = "sound bare ID and pitch"
        mc.playSound(0, 1, 1, "block.bell.use", pitch=0.75, receiver="world")
        passed("playSound bare block.bell.use pitch world")
        time.sleep(0.75)
        stage = "sound note"
        mc.playSound(0, 1, 1, "block.note_block.harp", note=18, receiver="self")
        passed("playSound note self")

        stage = "block sound target"
        original_block = mc.getBlock(3, 1, 0)
        if original_block["block_id"] in {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}:
            mc.setBlock(3, 1, 0, "stone")
            summary["temporary_block_remaining"] = True
            passed("temporary stone in previously empty position")
        stage = "playBlockSound defaults"
        mc.playBlockSound(3, 1, 0, "hit")
        passed("playBlockSound raw SoundGroup defaults")
        time.sleep(0.5)
        stage = "playBlockSound pitch"
        mc.playBlockSound(3, 1, 0, "hit", pitch=0.75, receiver="self")
        passed("playBlockSound pitch self")
        time.sleep(0.5)
        stage = "playBlockSound note"
        mc.playBlockSound(3, 1, 0, "hit", note=18, receiver="world")
        passed("playBlockSound note world")
        if summary["temporary_block_remaining"]:
            stage = "restore temporary block"
            mc.setBlock(3, 1, 0, original_block["block_id"], state=original_block["state"])
            summary["temporary_block_remaining"] = False
            passed("temporary block restored")

        stage = "human core frame observation"
        checkpoint("entity particle sound frames visible", "graph")
        stage = "frozen 3D graph sample"
        sample = FOLDER / "particle_graph_frozen.py"
        draw_graph = runpy.run_path(str(sample))["draw_graph"]
        before = sum(frame["direction"] == "send" and frame["method"] == "world.spawnParticle" for frame in frames)
        draw_graph(mc)
        after = sum(frame["direction"] == "send" and frame["method"] == "world.spawnParticle" for frame in frames)
        if after - before != 81:
            raise DiagnosticStop("graph did not emit exactly 81 particle requests")
        passed("frozen 3D graph sample", particle_requests=81)
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
        summary["frame_count"] = len(frames)
        if mc is not None:
            try:
                mc.close()
            except Exception as error:
                summary["close_failure_type"] = type(error).__name__
                summary["status"] = "FAIL"
        if frame_file is not None:
            frame_file.close()
        # On failure do not issue additional world calls. Report any leftovers.
        (FOLDER / "representative_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
