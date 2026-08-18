#!/usr/bin/env python3
"""Secret-safe live session-token persistence probe."""

from __future__ import annotations

import argparse

from mc_remote.connection import McRpcError
from mc_remote.minecraft import Minecraft


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("b3", "b4"))
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--no-pair", action="store_true")
    parser.add_argument("--auth-only", action="store_true")
    args = parser.parse_args()

    mc = Minecraft.create(
        address="127.0.0.1",
        port=args.port,
        sync_catalog=False,
        wirescope=False,
        pair=not args.no_pair,
    )
    try:
        assert mc.protocol == "21.0.0"
        if args.auth_only:
            print(f"PASS {args.phase} session-token authentication protocol=21.0.0")
            return
        if args.phase == "b3":
            try:
                mc.getPose()
            except McRpcError as exc:
                assert exc.code == -32601
                print("PASS rollback b3 player.getPose=method_not_found protocol=21.0.0")
            else:
                raise AssertionError("player.getPose unexpectedly succeeded on b3")
        else:
            pose = mc.getPose()
            assert set(pose) == {"world", "pos", "yaw", "pitch"}
            assert isinstance(pose["pos"], list) and len(pose["pos"]) == 3
            print("PASS b4 player.getPose=success protocol=21.0.0")
    finally:
        mc.close()


if __name__ == "__main__":
    main()
