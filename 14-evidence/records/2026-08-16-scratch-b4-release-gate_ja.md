# Scratch editor b4 release gate evidence

## Record

- test ID: `2026-08-16-scratch-b4-release-gate`
- test class: `unit/deterministic` + `live-human`
- result: **PASS / Scratch component b4 gate GREEN（横断b4 release gateは未完）**
- observed date: `2026-08-16`
- source repository: `Naohiro2g/scratch-editor`
- source branch: `release/b4`
- candidate: `56011f71291f47ced69cc4e3c377734f501b6081`
- release target: Scratch editor `2100.0.0b4`
- protocol: `21.0.0`
- decision: `2026-08-16-08`
- knowledge contract: `10-protocol/versioning-design_ja.md` §10.11.3 / `13-scratch-client/scratch-roadmap_ja.md` §3
- knowledge contract commit: `b747fa2b3b6c278f1a8e920ba8e02b45e2cf2b47`
- GitHub Actions: run `31934776981`

本recordはCatalog Picker、player pose、Scratch main stream 1件のMessageChannel観察、pose対応済み共通
WireScope artifact、candidate全体の回帰、rollback targetを一組として固定する。Pythonとの順次横断E2E、
plugin artifactの独立gate、home alpha、横断b4 release承認をPASSとはしない。

## Candidate and ancestry

- `develop`と`release/b4`はcandidate完全SHAに一致した。
- Catalog Picker実装`7cd936435520875729372bbbf28dd2f7266adb96`はcandidateのancestorである。
- player pose実装`0b74d16b9c18599c2526aec875febb746262e713`とlive-human source
  `182c4d243d693346f20416db1b7d9ab97167c389`はcandidateのancestorである。
- CI run `31934776981`はcandidate完全SHAでcompleted / successだった。

## Contract matrix

| b4 Scratch gate | Evidence / observation | Result |
| --- | --- | --- |
| authenticated catalog acquisition | 実browserで取得済みCURRENT catalogを確認 | PASS |
| `catalogHash`一致 | hash一致cacheだけをCURRENTとして使用し、不一致／invalidを拒否する回帰 | PASS |
| catalog failureのfail-open | catalog取得失敗でもMinecraft接続を継続 | PASS |
| 入力境界 | catalogなしの自由入力を維持し、reporter／変数等のnon-shadow入力を置換しない | PASS |
| resource表記 | vanillaは短縮形、非vanillaは完全修飾形 | PASS |
| picker操作 | 検索、選択、state編集、通常の編集可能文字列への適用 | PASS |
| `player.getPose` | paired playerの`{world,pos,yaw,pitch}`取得とblock表示 | PASS |
| `player.setPose` | `[world,x,y,z,yaw,pitch]`送信、適用済みpose result、yaw正規化を再解釈しない | PASS |
| WireScope観察 | `player.setPose` request／responseと状態変化をmain stream 1件として観察 | PASS |
| observer contract | validator、allowlist、session fixtureに両pose methodを収録 | PASS |
| Scratch handoff | MessageChannel adapterでcommon appへ接続し、substreamを生成しない | PASS |
| immutable artifact | clean checkoutから2回生成し、ZIP／manifestがbyte-for-byte一致 | PASS |
| security／license | secret／runtime値を含めず、AGPL本文、NOTICE、対応source導線を収録 | PASS |

## Catalog Picker live-human

実browserでMinecraft `1.21.11`の取得済みcatalogを開き、`door`検索から`bamboo_door`を選択し、stateを
編集して`bamboo_door[facing=east,half=lower,hinge=left,open=true,powered=false]`を通常の編集可能文字列として
適用できることを確認した。

- handoff manifest SHA-256: `385f4a6a5417b357bdb366a8e13458dda9d22c8bc36c40ee09958fe1f09fa3da`
- [catalog-picker-current-state.png](../artifacts/2026-08-16-scratch-b4-release-gate/catalog-picker-current-state.png)
  - SHA-256: `a345f639c12258f3250759806c1c5c9da07375c2476598e2130b87a21f4d9747`

画像は接続済みCURRENT状態、検索、state編集、構築した値を示す。画像だけでhash mismatch、reporter非置換、
`.sb3` round-tripを証明したとは扱わず、deterministic regressionと組み合わせる。

## Player pose live-human

Scratch Editor上のpose blockを実Minecraftへ適用し、WireScopeで`player.setPose`の送受信とMinecraftによる
yaw正規化を確認した。`player.getPose`の独立frame transcriptは収録していないため、block表示・実機確認と
deterministic fixtureを根拠とし、添付transcript単独の主張にはしない。

- handoff manifest SHA-256: `3fb509abfc32b69a758c584080b8d72d0dd6683269e5e7b0eb98730c6c1ff705`
- [wirescope-set-pose-sanitized.txt](../artifacts/2026-08-16-scratch-b4-release-gate/wirescope-set-pose-sanitized.txt)
  - SHA-256: `cd3329ed0a1e58cf7467392a6361134c0c4cf6221cf2a6ab67dd328d08a32f2e`

## WireScope artifact identity

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `wirescope-app.zip` | 53,552 | `1a56617c78c283332f1afe3bdd3797ab37f0cdc3455c86c73c926c751721657f` |
| `wirescope-app.manifest.json` | 2,321 | `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154` |

- source: `56011f71291f47ced69cc4e3c377734f501b6081`
- Node: `24.19.0`
- recipe: `npm ci && npm run build:artifact --workspace=@mc-remote/live -- --source-commit 56011f71291f47ced69cc4e3c377734f501b6081`
- handoff manifest SHA-256: `8d99b192f62e4eb424852e3c9d9113789f16a12e760341b8e3b56d71b7e5dc03`
- [wirescope-app.manifest.json](../artifacts/2026-08-16-scratch-b4-release-gate/wirescope-app.manifest.json)
  - SHA-256: `f3ec11496b595bbca4ba27a6e938a1149336eb5a2da55e742d60e1681cf4d154`

ZIP本体はknowledgeへ複製しない。manifestのarchive hash、source commit、recipe、asset inventory、license、
対応source URLを公開し、同じpairを収録したPython wheel／将来release artifactを配布identityとする。
Python b4 candidate evidenceのZIP／manifest hashも本pairと一致する。ただし両sourceを順に操作した横断E2Eは
別gateである。

## Deterministic and CI results

- `@mc-remote/live`: lint PASS、9 files／51 tests PASS、build PASS
- `@mc-remote/protocol`: lint PASS、1 file／5 tests PASS、build PASS
- Scratch VM catalog: 6 subtests／9 assertions PASS
- Scratch VM McRemote extension: 63 subtests／187 assertions PASS
- Scratch GUI b4関連: 12 suites／64 tests PASS
- Scratch GUI full unit: 61 suites／400 tests PASS、1 skipped、15 snapshots PASS
- Scratch GUI lint: 0 errors（既存931 warnings）
- Scratch VM build: PASS（既存optional `canvas` warningのみ）
- Scratch GUI dev／dist／standalone build: PASS（既存asset-size warningsのみ）
- GitHub Actions run `31934776981`: Build、全package test、Test ResultsがPASS
- `git diff --check`: PASS

## Security, compatibility, and rollback

- protocolは`21.0.0`を維持し、`streams[]`を前方互換の器として保つがsubstreamを実装していない。
- artifactへpair code、credential、player UUID、runtime port、attach codeを含めていない。
- screenshotとtranscriptへpair code、credential、player UUID、observation grant、private hostを含めていない。
- rollback targetは`v2100.0.0b3@3f1a10a366bfbe76e32b5a31c54da19eddd56e56`として存在する。
- hosted surface更新、rollback実操作、b4候補への再復帰は本recordで実施していない。

## Remaining cross-component b4 gate

- ScratchとPythonで同じartifactを順に使う横断real-browser E2E
- exact plugin artifact／JAR identityを含む最終compatibility set照合
- home alphaでの接続、Picker、pose、観察、故障切り分けの一巡
- component rollback実操作とb4候補への再復帰の要否・結果
- tag／GitHub prerelease作成とrelease後identity確認

以上の横断項目を満たすまで、本recordから横断b4 milestoneのGREENを推測しない。
