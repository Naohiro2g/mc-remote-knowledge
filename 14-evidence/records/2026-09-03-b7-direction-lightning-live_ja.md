# b7 direction／lightning live gate evidence（client segment）

> status: Python segment PASS。Scratch segment実施中。McRemote plugin側の同機能blocker解消は
> [2026-09-01 record](2026-09-01-b7-direction-lightning-live_ja.md)のaddendumで既にCLOSED。

## Record

- test ID: `2026-09-03-b7-direction-lightning-live`
- test class: `live-auto` + `live-human`
- observed date: `2026-09-03` JST
- result（Python segment）: **PASS**
- protocol: `23.1.0`
- artifact version: `2301.0.0b7`
- contract: `10-protocol/wire-format-design_ja.md` §5.8.2
- decisions: `2026-09-01-01`、`2026-09-01-02`、`2026-09-02-01`、`2026-09-02-02`
- target: `m720s2-dev-integration`（host-native、既存稼働中）
- exact set: `b7-integrated-artifact-set-1`（`release-gate-notes_ja.md` 2026-09-02 b7節）

## Fixed input（Python segment）

| 面 | identity |
| --- | --- |
| McRemote JAR | `mc-remote-1.21.11-2301.0.0b7.jar`、222,951 bytes、SHA-256 `f08388cf393e02db1eb605e707dfaec890792e7a475de5a51caacbc940028ee9` |
| Python | branch`codex/b7-wirescope-set2@91a25d317c95570fd9d92b5e63a5f585a856eda3`、wheel 196,970 bytes、SHA-256 `81540d22b1ee05d7b24bd2e6c9270a37a194c6c1ddc868148a8263624826d2ba` |

private endpoint、token、pairing identity、player UUID等の秘密実値は素材の時点で`"endpoint": "redacted"`
として既に除去されている。player座標はtest world内の非秘匿gameplay値、entity handleは opaque識別子であり
収録する。

## 経過と結果

1. **初回試行（PASS→harness crash）**: `player.getDirection`／`setDirection([1,0,0])`／`getDirection`はRPCとして
   PASSしたが、人間観察は`NO_VISIBLE_CHANGE`（判定不能）だった。続けて`setDirection([0,0,0])`を送り、
   contractどおり`zero_direction`エラーを受理（**PASS**）。直後、test harness自身が`KeyError: '0'`で停止した。
   これはMcRemote plugin／protocolの契約違反ではなく、Python側test runnerの例外処理不足である。
2. **承認済みrerun（PASS）**: `[-1,0,0]`で再試行し、`CLEAR_VISIBLE_CHANGE`を人間が確認。RPC・post-read一致。
3. **resume segment（PASS）**: `world.spawnEntity`でarmor stand生成→`entity.getDirection`／`setDirection([1,0,0])`／
   `getDirection`往復がPASS。続けて`world.strikeLightning`がexact targetへ`result:null`を返し、人間が
   flash／soundを確認（**PASS**）。
4. **人間観察サマリ**: directionはrerun後にPASS判定、lightningは視聴覚ともPASS。
   改善案（30度刻み回転、同一地点への固定落雷目印）はnon-blocking follow-upとして記録するのみ。

## 判定

Python client segmentは**PASS**。初回のharness `KeyError`はcontract／製品FAILに数えない。McRemote plugin側の
direction／lightning contract blocker（外部dimension移動時のreason誤判定、孤立`mcr.lightning`）は
2026-09-01 recordのaddendumで既にCLOSED、今回の対象外。

## Sanitized artifact

- [python-initial-attempt.json](../artifacts/2026-09-03-b7-direction-lightning-live/python-initial-attempt.json)
  - SHA-256: `8f87d4bfad2fc707866d411ee92873996cd28c691292a51ba12245428ffe7732`
- [python-direction-rerun.json](../artifacts/2026-09-03-b7-direction-lightning-live/python-direction-rerun.json)
  - SHA-256: `25f3f54161715438af9e4380ee0ae089badbd7c0834b1d27915bbdea98ea97d1`
- [python-resume-entity-lightning.json](../artifacts/2026-09-03-b7-direction-lightning-live/python-resume-entity-lightning.json)
  - SHA-256: `f09b822f56ab493780b75371b916ad38ccf2deb2435bfbaec8ad486e37e04d41`
- [python-human-observation.json](../artifacts/2026-09-03-b7-direction-lightning-live/python-human-observation.json)
  - SHA-256: `36a4bf0d5a7fce19e981caf7236ebd94d303c2e2593d01c205f23795c0e8bc1d`

artifactは判定、固定source／artifact identity、公開可能なRPC frame、人間観察分類だけを収録する。token、
private endpoint、pairing identity、player UUIDは収録しない。

## Non-claim

- Scratch／WireScope real-browser segment（別途進行中、本recordへ追記予定）
- rate limit本較正、capacity／soak
- 全回帰、default branch統合、tag、公開release
- Python test harnessの`KeyError`修正自体（follow-upとして別途扱う）
