# Python b3 catalog / projection live-human evidence

## Record

- test ID: `2026-08-06-b3-python-catalog-projection-live-human`
- test class: `live-human`
- result: **PASS（下記 Claim boundary の範囲）**
- observed from: `2026-08-06T17:25:27+09:00`
- observed to: `2026-08-06T17:31:24+09:00`
- source repository: `Naohiro2g/minecraft-remote-api`
- source branch: `protocol-21.0.0-b3`
- Python candidate: `af2d11d66a16e3085f569241406a703a1c28c348`
- Python package version: `2100.0.0b3`
- protocol: `21.0.0`
- knowledge contract commit: `1d10c773452a2b58255faeeebed0eec427c3023a`

秘密実値は含まない。placeholder、除去対象、保持した非 secret identity は
[redactions.json](../artifacts/2026-08-06-b3-python-catalog-projection-live-human/redactions.json) に固定した。
raw terminal transcript、token store、生成された catalog / projection 本体、build artifact 本体は
knowledge へ搬送していない。

## Anchor の性質と受理判断

Python candidate commit は GitHub remote で存在を確認した。稼働 plugin は次の二段 anchor とする。

1. **一次 anchor**: deployed JAR SHA-256
   `aeb190705bd9957ce73557dc1be0fe15efe7250ba9bc688945e6f537e00ef78e`
2. **二次 anchor**: plugin commit
   `a3dab998b710f65f42f95058a68ec51d419b097c`

plugin commit は共有 workspace の `Naohiro2g/McRemote` repository、local branch
`feature/long-lived-credential` に実在することを確認したが、2026-08-06 の着地時点で GitHub API からは
到達できなかった。plugin version、commit、deployed JAR digest、Paper / Minecraft version は deploy 側の
人間確認値である。このため本 record は、**固定された JAR と Python candidate の間で下記挙動が観測された**
ことを根拠化するが、JAR が remote commit から再現可能に build できること、plugin b3 の release readiness、
plugin commit の remote 固定までは主張しない。

sdist / wheel、live 生成した catalog、`mc_constants.py`、projection manifest の本体も搬送していない。
[checksums.txt](../artifacts/2026-08-06-b3-python-catalog-projection-live-human/checksums.txt) は実測時に固定した
digest declaration であり、本 record 内で対象 binary / generated file を再 hash した結果ではない。
一方、sanitized transcript、summary、機械可読結果は knowledge 側で material identity を hash 固定した。

## Subject identity

| Subject | Identity |
| --- | --- |
| Python source | `protocol-21.0.0-b3@af2d11d66a16e3085f569241406a703a1c28c348` |
| Python package | `minecraft-remote-api==2100.0.0b3` |
| protocol | `21.0.0` |
| McRemote plugin version | `1.21.11-2100.0.0b3` |
| McRemote plugin commit | `a3dab998b710f65f42f95058a68ec51d419b097c`（local commit、remote未到達） |
| deployed JAR SHA-256 | `aeb190705bd9957ce73557dc1be0fe15efe7250ba9bc688945e6f537e00ef78e` |
| Paper | `1.21.11-130-ver/1.21.11@c5a2736` |
| Minecraft | `1.21.11` |
| Bridge | N/A（Python client / McRemote plugin の直接構成） |
| server | `[LOCAL_TEST_SERVER]` |
| world / build origin | `overworld` / `(200, 0, 200)` |

## Claim boundary

| Claim | Observation | Result |
| --- | --- | --- |
| human pairing | Python が提示した一時 code を人間が Minecraft 内で実行し、pairing 完了 | PASS |
| authenticated hello | protocol `21.0.0`、Minecraft `1.21.11`、`catalogHash` を受領 | PASS |
| `catalog.get` | network から block / entity / particle catalog を取得 | PASS |
| catalog hash | 宣言 hash、Python 再計算 hash、cache file 名が一致 | PASS |
| catalog validation | block 1166 / entity 157 / particle 115 を schema validation | PASS |
| projection | `mc_constants.py` と manifest を生成し、manifest 記載 digest と実 file が一致 | PASS |
| generated constants | block / entity / particle namespace を import。`ITEM_FRAME` / `VIBRATION` を照合 | PASS |
| cache reuse | network 取得後の `--no-pair` 再同期で `catalog_source=cache` | PASS |
| state 付き `block_ref()` | oak stairs の north / east / west / south と canonical full state を4地点で往復 | PASS |
| world restore | 保存した元状態へ4地点を完全復元。clear / place / restore status は全て0 | PASS |

hello の `catalogHash` は
`6d0f8524b70e37fb8d7b34d0fdb45c2b058dcfea82920d86ca9aaabb9fcadc83`。
projection key は
`31dda5aa5af4783a4515440cd1afa347d2e32ccf0015849b76240ab9d30abccf`、
generator version `1`、projection schema version `1` だった。

初回の未認証接続は応答前に close した。再接続後に所定の auth-required / pairing flow が成立し、
正式シナリオはその再試行から PASS とした。失敗を無かったことにはせず、時系列 artifact に残した。

## Supporting candidate gate results

同じ Python candidate について、搬送元は次を報告した。

- b1: 13/13 PASS
- b2: 27/27 PASS
- b3: 40/40 PASS
- sdist / wheel build: PASS
- sdist SHA-256:
  `710e6285b295dee1fd9da44685a36607c1e4620a18f03f490d621cc8dca4258b`
- wheel SHA-256:
  `1292944afa6dc67f407f34e8eabf29f080c8a45739ae7eba6593f8666e0c3a61`
- projection生成物は配布物へ同梱していない

これら unit / deterministic test の正式根拠はcandidate内のtest code、PASS command、candidate commitであり、
本live-human recordは別JSON test artifactを必須化しない `2026-07-06-03` の扱いを変更しない。

## Human checkpoints

人間は pairing 開始と、read-only preflight 後の4地点に対する
`air → state付きstairs → 元状態復元` をそれぞれ明示承認した。Minecraft内でpairing commandを実行し、
deploy側のplugin / JAR / Paper / Minecraft identityを確認した。agentは隔離source / credential / cache /
projection出力先の準備、catalog / projection検証、対象4地点のpreflight・操作・復元確認、sanitizationを担当した。

## Sanitized artifacts

- [live-summary_ja.md](../artifacts/2026-08-06-b3-python-catalog-projection-live-human/live-summary_ja.md)
  - SHA-256: `744f4d1b178c4e8544260808304fb97375d1e95fa493a287ed5146bf5a9b9000`
- [sanitized-transcript_ja.md](../artifacts/2026-08-06-b3-python-catalog-projection-live-human/sanitized-transcript_ja.md)
  - SHA-256: `f41f8fc91fcdc38fb1882c9102c7caeb862522f4734ac2bed8fa1f53c9ecb24a`
- [live-results.json](../artifacts/2026-08-06-b3-python-catalog-projection-live-human/live-results.json)
  - SHA-256: `f4e1676e3a6c15acda466f4df730213e79891d6492f29f44103e72c82b66455c`
- [checksums.txt](../artifacts/2026-08-06-b3-python-catalog-projection-live-human/checksums.txt)
  - SHA-256: `19a95c5abd0acd38f404c4c434e22dc1d93292af2899e1fa421d01a0a01c354b`
- [redactions.json](../artifacts/2026-08-06-b3-python-catalog-projection-live-human/redactions.json)
  - SHA-256: `2faa4e8dd763480abfaa1925aff037c41187937dff44ef4fc2b2c4ad6477419b`

`live-summary_ja.md` は正式配置に合わせ、搬送元の `materials/checksums.txt` 参照を同directoryの
`checksums.txt` へ正規化した。それ以外の搬送material本文は同一である。

## Redaction boundary

pairing code、authentication token、token-store内容、player UUID、private host / port / 接続情報、
workspace / credential store / cache / raw を含むfilesystem絶対local pathを除去またはplaceholder化した。
rawはsource側private local storageにだけ保持し、knowledgeへ搬送していない。

公開component version / commit、JAR digest、protocol、Minecraft / Paper version、catalogHash、projection key、
生成物digest、件数、試験座標、canonical block state、PASS / FAIL観測はclaimを束縛する非secret値として保持した。

## 未検証の境界

- `permission_denied` とtoken温存のlive確認
- 実機rollback
- GitHub tag / prerelease作成後の配布確認
- TestPyPI / PyPI公開
- entity spawn / particle emit（現行b3 Python API surface外）
- plugin commitのremote固定と、deployed JARのcommit-exactな再現build
- McRemote plugin、Stack、Scratchそれぞれのb3 release readiness

## Release gate での扱い

本recordを、Python candidate `af2d11d66…` のcatalog / projectionに対する正式live-human根拠として受理する。
これにより「repo-local NOTESに観測はあるが、plugin identity、sanitized transcript、正式recordが無い」という
Python b3 gateのevidence gapを閉じる。ただし本record自体はtag / GitHub prereleaseの作成、PyPI公開、
他componentのb3完了を意味しない。Python dev側が着地内容を照合し、残るrelease操作前checkを確認した後に
Python component固有の最終release可否を判定する。
