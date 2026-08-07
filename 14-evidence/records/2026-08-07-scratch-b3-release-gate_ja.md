# Scratch editor b3 release gate evidence

## Record

- test ID: `2026-08-07-scratch-b3-release-gate`
- handoff ID: `2026-08-07-scratch-b3-3f1a10a`
- test class: `unit/deterministic` + `live-auto` + `live-human`
- result: **PASS / Scratch component b3 gate GREEN（下記境界内）**
- observed date: `2026-08-07`
- source repository: `Naohiro2g/scratch-editor`
- source branch: `release/b3`
- candidate: `3f1a10a366bfbe76e32b5a31c54da19eddd56e56`
- release target: Scratch editor `2100.0.0b3`
- protocol: `21.0.0`
- knowledge contract: `13-scratch-client/scratch-roadmap_ja.md` §2.3 / `2026-07-08-03`
- knowledge contract commit: `3dfbf57c07f2b7985c65edc5564b879f9e67e122`
- GitHub Actions: run `31145335984`

秘密実値は含まない。placeholder、除去対象、保持した非secret identityは
[redactions.json](../artifacts/2026-08-07-scratch-b3-release-gate/redactions.json)へ固定した。
ユーザー貼付raw、token、pair code、pairing ID、private host、player UUIDはknowledgeへ搬送していない。

## Candidate とremote anchor

2026-08-07の着地確認時に、GitHub remoteの`release/b3`がcandidate完全SHAと一致することを確認した。
CI run `31145335984`も同じ`head_sha`でcompleted / success、次の全jobがsuccessだった。

- `Build`
- `Test / Test scratch-gui`
- `Test / Test Results`

candidateは`c497e06983`基点から次の3 commit、6 file、154 insertions / 23 deletionsに限定される。

1. `231fca64eb` — loopback WebSocket development
2. `458b76e0c1` — persisted connection target初期化
3. `3f1a10a366` — GUI lint適合

b4送りのcatalog picker、WireScope mini、roadmap文書はcandidateへ含めない。独立WireScopeも未実装だが、
`2026-08-06-03`によりb3 blockerではない。

## Live environment anchor

| Subject | Identity |
| --- | --- |
| McRemote plugin version | `1.21.11-2100.0.0b3` |
| McRemote plugin commit | `a3dab998b710f65f42f95058a68ec51d419b097c` |
| deployed JAR SHA-256 | `aeb190705bd9957ce73557dc1be0fe15efe7250ba9bc688945e6f537e00ef78e` |
| Paper | `1.21.11-130-ver/1.21.11@c5a2736` |
| Minecraft | `1.21.11` |
| transport | test Bridge 1件、Localhost / private Devの2 Sandbox route |

plugin commitは2026-08-07にGitHub remoteで存在を確認した。deployed JAR digestとPaper / Minecraft identityは
deploy側の人間確認値である。本recordは固定されたJARとのlive相互運用を根拠化するが、JARのcommit-exactな
再現buildやplugin自身のb3 release readinessまでは主張しない。

## Contract matrix

| §2.3 gate | Evidence / observation | Result |
| --- | --- | --- |
| 全体lint | scratch-gui full lint exit 0 / errors 0。908 warningsはupstream既存として分離 | PASS |
| McRemote scope lint | changed scope 0 errors / 0 warnings、例外規則なし | PASS |
| runtime config正常系 | deployment JSONのload / normalize、loopback WS許可条件をunitで確認 | PASS |
| runtime config欠落・HTTP failure | JSON取得404を`connectionEnabled=false` / `runtime-config-unavailable`へfail-close | PASS |
| runtime config schema failure | default target欠落、label欠落、notice必須field欠落、非HTTP(S) linkをfail-close | PASS |
| token非読出し / WebSocket非生成 | disabled configのVM unitとbuilt browser smokeで、token非読出し、socket 0件 | PASS |
| 生成HTML inventory | showcase公開entryは`index.html`のみ。除外HTML / bundle 8 URLは404 | PASS |
| showcase説明 | notice heading / bodyをbuilt browserで確認 | PASS |
| showcase全公開URL fail-close | build-time disable + runtime `connection_enabled=false`。connect reason `connection_disabled` | PASS |
| `.sb3` serialization regression | VM state snapshot 117 fixtures / 117 PASS | PASS |
| pair / token reconnect | Dev routeで新規pairing、reload後に再pairingなしで接続 | PASS |
| 接続先別token | Localhostで新規token取得後もDev tokenを保持し、Dev復帰時に再利用 | PASS |
| `permission_denied` token温存 | deny後もtokenを破棄せず、権限復帰後に再pairingなしで接続 | PASS |
| 設定先 / 実接続先 | route切替前後の不一致・再接続要・再接続後一致をパレットで確認 | PASS |
| WireScope / パレット状態 | candidate identity、接続状態、設定先 / 実接続先、再接続状態を通常版で目視 | PASS |

## Deterministic results

- scratch-gui related: 6 suites / 28 tests PASS
- scratch-gui full unit: 56 suites / 372 tests PASS、1 skipped、15 snapshots PASS
- scratch-gui full build: PASS
- scratch-vm McRemote: 52 subtests / 147 assertions PASS
- VM state snapshot: 117 / 117 PASS
- `git diff --check`: PASS

full buildのdist / standalone asset-size warningとfull lintの908 warningsはupstream既存であり、今回変更起因は0。
最終candidateでscratch-vm McRemote unitとstate snapshotを再実行している。

## Live-auto showcase

`MCREMOTE_SHOWCASE=true`でbuildし、Pages artifact pruneとruntime config rewriteをcandidate identity付きで実行した。
loopback HTTP fixtureに対するHTTP matrixは`/`、`/index.html`、runtime configの3 URLが200、除外対象のHTML /
bundle 8 URLが404。保存したPlaywright scriptによるheadless Chromium smokeで、notice、connect block、
`connection_disabled`、`connectionEnabled=false`、candidate identity一致、WebSocket 0件を確認した。

in-app Browserは当該環境の信頼境界で利用不能だったため、保存済みscriptをfallbackとして採用した。
これは人間操作を要しないbuilt artifact smokeであり、`live-auto`として受理する。

## Live-human

### Dev pairing / token reconnect

2026-08-07 13:19 JST。operator操作前に期限切れとなった先行attemptは正式観測から除外し、新しいpairingを実施。
candidate SHAをclient versionに持つ認証済みhelloが成功し、同browser windowのreload後は再pairingなしで接続した。

### `permission_denied` token preservation

2026-08-07 13:40–13:41 JST。paired playerの`mcr.online`を無効化するとreason `permission_denied`を受領。
権限復帰後、保存済みDev route tokenで再pairingなしに接続し、token温存を確認した。

### Target-specific token

2026-08-07 13:48 JST。DevからLocalhostへ切り替え、新しいLocalhost pairing / tokenを成立させた後も、
Dev route tokenは上書きされなかった。Devへ戻すと再pairingなしで再利用され、切替中の設定先 / 実接続先不一致、
再接続要、接続後一致を表示した。

## Security / compatibility / rollback

- `ws:`はHTTP loopback pageからloopback Bridgeへのdevelopment経路だけ許可する。
- HTTPS page、非loopback page、非loopback Bridgeへの平文WSは拒否し、公開経路は`wss:`を維持する。
- showcaseはbuild-time disableとruntime configの二重fail-closeで、tokenを読まずWebSocketを生成しない。
- pairing code、token、pairing ID、private host、player UUIDをevidenceへ保存しない。
- protocolはclean `21.0.0`のまま。
- `.sb3` / VM state compatibilityは117 snapshotで確認した。
- rollback先`v2100.0.0b2`はcommit `e19247069d1ae55037c0e9ffc52ea88cde612ac3`のGitHub prereleaseとして存在する。

## Sanitized artifacts

- [deterministic-summary_ja.md](../artifacts/2026-08-07-scratch-b3-release-gate/deterministic-summary_ja.md)
  - SHA-256: `3b95541d196922d228b8dde440ed2685c2254b5639fe944fb7bd78fe2fa900dd`
- [live-auto-showcase_sanitized_ja.md](../artifacts/2026-08-07-scratch-b3-release-gate/live-auto-showcase_sanitized_ja.md)
  - SHA-256: `638affe85587d64077a107c7a209aca745a567fccbecc4ceafb1c065e361dc12`
- [live-auto-showcase-smoke.cjs](../artifacts/2026-08-07-scratch-b3-release-gate/live-auto-showcase-smoke.cjs)
  - SHA-256: `82efe0955eb3c6d801ce74c0259f9e846191b1fb25b73dcdd24c72ccf0f50965`
- [live-human-dev-pair-token-reconnect_sanitized_ja.md](../artifacts/2026-08-07-scratch-b3-release-gate/live-human-dev-pair-token-reconnect_sanitized_ja.md)
  - SHA-256: `8d97133e2b05296ff47cb3c4623d4832522f3f972faef69def72d38caa6276ab`
- [live-human-permission-denied-token-preservation_sanitized_ja.md](../artifacts/2026-08-07-scratch-b3-release-gate/live-human-permission-denied-token-preservation_sanitized_ja.md)
  - SHA-256: `2695944c43f9abd702fb9073802c5f87366a06a21d9eeddaecebe11f698954dd`
- [live-human-target-specific-token_sanitized_ja.md](../artifacts/2026-08-07-scratch-b3-release-gate/live-human-target-specific-token_sanitized_ja.md)
  - SHA-256: `6e3c4a8a59176ed3c3cf10f639eff08a05684536678c7ec3bcbc3ff00dd989a2`
- [redactions.json](../artifacts/2026-08-07-scratch-b3-release-gate/redactions.json)
  - SHA-256: `f344dc73963267952ab7813be5c74fe05c346e5d8d456cbe8ec6a8bebd46f56a`

`live-auto-showcase_sanitized_ja.md`は正式配置に合わせ、搬送元の
`materials/live-auto-showcase-smoke.cjs`参照を同directoryのfile名へ正規化した。それ以外の搬送material本文は同一。

## Redaction boundary

pairing code、authentication token、pairing ID、private host / port / route identity、player UUID、
ユーザー貼付rawを除去または非収集とした。live transcript内のtokenは`[redacted]`、private endpointは
`private Dev route` / `Localhost route`という意味を保持する分類へ置換した。

公開component version / commit、JAR digest、protocol、Minecraft / Paper version、candidate SHA、CI run ID、
test件数、HTTP status matrix、stable error reason、PASS / FAIL観測はclaimを束縛する非secret値として保持した。

## 未検証の境界

- `v2100.0.0b3` tag / GitHub Release作成後のidentity・flag確認
- hosted surfaceのdeploy smoke、rollback、再deploy
- 独立WireScope（`2026-08-06-03`によりb3 blockerではない）
- catalog picker / WireScope mini（b4送り。candidateに非収容）
- McRemote plugin、Stack、Python APIそれぞれのrelease readiness
- deployed JARのcommit-exactな再現build

一時Scratch HTTP surfaceと2 target検証用の一時Bridgeは停止済み。hosted surfaceは更新していないため、
本gateでhosted rollback操作は要求しない。将来hosted surfaceを更新する場合は、その時点のexact source /
artifact identity、deploy smoke、rollback、再deployを別途確認する。

## Knowledge release gate 判定

Scratch roadmap §2.3の全項目に正式evidenceが対応し、security / compatibility / rollback境界も明示された。
したがって、**Scratch editor component `2100.0.0b3`のGitHub prerelease gateをGREENとする**。

許可するrelease操作は次に限定する。

- tag `v2100.0.0b3`をcandidate `3f1a10a366bfbe76e32b5a31c54da19eddd56e56`へ作成する。
- GitHub Releaseをprerelease ON、draft OFFで作成し、Latestにしない。
- hosted surfaceの更新をこのrelease操作へ自動的に含めない。
- rollback先を`v2100.0.0b2`とする。

release後はtag target、release URL、prerelease / draft / Latest状態を確認し、NOTESを本recordとknowledge commitへ
接続する。異なるcandidateへのtag、candidateへの追加commit、hosted deployの同時実施は本GREEN判定の範囲外とする。
