# b4 Python player pose／WireScope live-human evidence

## Record

- test ID: `2026-08-16-b4-python-pose-wirescope-live-human`
- test class: `unit/deterministic` + `live-human`
- result: **PASS / Python b4 component candidate（横断b4 release gateは未完）**
- observed date: `2026-08-16`
- source repository: `Naohiro2g/minecraft-remote-api`
- source branch: `codex/b4-player-pose`
- candidate: `4d510442db58a94f8b249ddcd9d959381f97276c`
- release target: Python `2100.0.0b4`
- protocol: `21.0.0`
- decision: `2026-08-16-08`
- knowledge contract: `12-python-client/python-client-guide_ja.md` / `15-wirescope/wirescope-station-attach-design_ja.md`
- knowledge contract commit: `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`

本recordは、固定candidate wheelから起動したPython main stream 1件のpose操作とWireScope観察を根拠化する。
Scratch sourceとの横断E2E、home alpha、rollback実操作、tag／release作成をPASSとはしない。

## Exact compatibility set

| Component | Identity |
| --- | --- |
| Python source | `4d510442db58a94f8b249ddcd9d959381f97276c` |
| Python wheel SHA-256 | `eeed6261972987946b5e22dd8ff8d3533a758c7db57472d1d82766fbf964e7d0` |
| Python sdist SHA-256 | `f64528a9a8dfa83fea715c940f69562d263796c9e6947ee65a8f506b0a228477` |
| McRemote source | `9df8c46d600ff9605dc1822b304715de713e6767` |
| McRemote JAR version | `1.21.11-2100.0.0b4` |
| McRemote JAR SHA-256 | `ab3b87c38b6876ec4ba26112eff35d7cb016395a1dae1661578fd3690e1dbc46` |
| WireScope / Scratch source | `56011f71291f47ced69cc4e3c377734f501b6081` |
| WireScope ZIP SHA-256 | `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f` |
| WireScope manifest SHA-256 | `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154` |

## Live-human procedure and result

1. candidate commitからwheel／sdistを生成し、fresh venvへwheelをinstallした。
2. installed packageからrunnerを起動し、一時credential directoryでpairingした。
3. automatic browser launchからloopback stationの共通WireScope appへattachした。
4. `player.getPose`のshapeと、build origin変更前後のorigin相対座標を確認した。
5. `player.setPose`のyaw正規化、pitch境界`-90`／`90`を確認した。
6. pitch範囲外と引数不足が`-32602 invalid_params`となり、失敗前後でposeが不変であることを確認した。
7. WireScope UIでhello、pose、origin変更、成功response、error responseをmain stream 1件として確認した。
8. `mc.close()`後に観測元終了とストリーム終了が表示されることを確認した。
9. 接続時のoriginとposeを復元し、一時credential directoryを削除した。

最終結果は`LIVE-HUMAN B4 POSE + WIRESCOPE PASS`だった。

## Deterministic and distribution results

- Python全回帰: `175 passed`
- `uv lock --check`: PASS
- wheel／sdist build: PASS
- wheel artifact／metadata／`RECORD`／license検査: PASS
- `git diff --check`: PASS
- candidate worktree: clean
- candidate remote SHA: 一致確認済み
- distribution license expression: `MIT AND AGPL-3.0-only`
- WireScope corresponding source導線: PASS
- WireScopeなしの既存経路への非介入: PASS
- observer起動／browser起動失敗時のMinecraft fail-open: PASS
- strict bootstrap／NDJSON／security headers: PASS
- top-level URLへのsecret非配置: live-humanで確認

## Security, compatibility, and rollback boundary

- protocolは`21.0.0`を維持し、substream機構を追加していない。
- pair code、attach code、credential／token、player UUID、private host、loopback port、接続時の座標と向きを収録していない。
- Python候補はmain stream 1件だけを生成・観察する。
- rollback候補は`v2100.0.0b3@af2d11d66a16e3085f569241406a703a1c28c348`である。
- rollback実操作とb4候補への再復帰は未実施である。

## Sanitized artifact

- [summary.json](../artifacts/2026-08-16-b4-python-pose-wirescope-live-human/summary.json)
  - SHA-256: `3fb08e58f53f08236ff597e4148af7ffd37fe113c489d91076a18200f2f7b7e4`

## Remaining b4 gate

- Scratch b4 candidateとCatalog Picker／poseの正式evidence
- 同じcommon app artifactを使うScratch MessageChannel regressionとの横断real-browser E2E
- home alphaでの接続、Picker、pose、観察、故障切り分けの一巡
- Python rollback実操作とb4候補への再復帰
- exact cross-component compatibility setの最終批准
- tag／GitHub prerelease作成とrelease後identity確認

以上が揃うまで、本recordだけでPython tagまたは横断b4 releaseをGREENにしない。
