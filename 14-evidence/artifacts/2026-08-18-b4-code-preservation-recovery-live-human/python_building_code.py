#!/usr/bin/env python3
"""Deterministic building-code fixture for b4 empty-environment recovery."""

from __future__ import annotations

import argparse
import os
import tempfile

from mc_remote.minecraft import Minecraft, PROTOCOL


EXPECTED_BLOCKS = {
    (4, 90, 0): "minecraft:lapis_block",
    (5, 90, 0): "minecraft:redstone_block",
    (6, 90, 0): "minecraft:diamond_block",
}


def _arguments():
    parser = argparse.ArgumentParser(
        description="Replay deterministic Python building code on an empty environment."
    )
    parser.add_argument("--address", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    return parser.parse_args()


def main():
    args = _arguments()
    mc = None
    previous_config = os.environ.get("MCREMOTE_CONFIG_DIR")
    with tempfile.TemporaryDirectory(prefix="mcremote-b4-code-reuse-") as config_dir:
        os.environ["MCREMOTE_CONFIG_DIR"] = config_dir
        try:
            mc = Minecraft.create(
                address=args.address,
                port=args.port,
                sync_catalog=False,
            )
            assert mc.protocol == PROTOCOL == "21.0.0"
            mc.setWorld("overworld")
            mc.setBuildOrigin(0, 0, 0)

            for position, block in EXPECTED_BLOCKS.items():
                mc.setBlock(*position, block)

            for position, expected in EXPECTED_BLOCKS.items():
                actual = mc.getBlock(*position)
                if actual != expected:
                    raise AssertionError(
                        f"block mismatch at {position}: expected={expected} actual={actual}"
                    )

            print(
                "PASS python building-code reuse "
                f"protocol={mc.protocol} blocks={len(EXPECTED_BLOCKS)}"
            )
        finally:
            if mc is not None:
                mc.close()
            if previous_config is None:
                os.environ.pop("MCREMOTE_CONFIG_DIR", None)
            else:
                os.environ["MCREMOTE_CONFIG_DIR"] = previous_config


if __name__ == "__main__":
    main()
