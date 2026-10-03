# b9移管の起点：公開b8 sourceのfixture一覧

- 採取元: scratch-editor@`691576f60b7f0824e1753bd6823901d01fbe2422`（tag `v2320.0.0b8`／developの公開target）。branch先頭`01cdb0b`は採取元ではない。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`のb8 CLOSED節、`10-protocol/protocol-tooling-migration-plan_ja.md`。
- knowledge contract commit: CLOSED節`2a8c3eae4e489e67f044111b0d1e6cdd22ead86a`、最新runtime／INDEX／移管計画`90cf87fbcd132984ef027a98a263e5911aaf30bf`を実際に読んだ。
- Protocol 7、WireScope 4、Bridge 1の計12 fixture。`git show <source>:<path>`の生bytesからSHA-256を算出し、既存の凍結後棚卸しの全12件と一致。
- case数はfixture内の明示case ID、または名前付きcase groupを数える。統一case定義のないfixtureは「未定義」とし、NDJSONの行数／snapshot数／辞書語数をcase数へ換算しない。

| owner | path | bytes | SHA-256 | case数 |
| --- | --- | ---: | --- | --- |
| Bridge | `mc-remote/bridge/test/fixtures/one-shot-transport-v1.json` | 517 | `018d8fc8201dc8bf5689c53549df7be62b78c7e1d07e553f60c869a9ebcf7ec5` | 未定義 |
| WireScope | `mc-remote/live/test/fixtures/display-alias-v1.json` | 322 | `85c8159a8b74788c0cf978078094d23a3cdae83c0be5e9aa9552bb820c8389ca` | 未定義 |
| WireScope | `mc-remote/live/test/fixtures/observer-session-lifecycle.ndjson` | 2,691 | `4fb06188a97025248cf5deea3ff9e50578d08136f079428d9bbac86ca920680b` | 未定義 |
| WireScope | `mc-remote/live/test/fixtures/scratch-main-lifecycle.json` | 5,100 | `3fe467c4e91fcbc2ccdee56a298d46b1b9dd7a1b4c2dfd0e9504ac2e6f609e2d` | 未定義 |
| WireScope | `mc-remote/live/test/fixtures/station-attach-v1.json` | 2,437 | `b50ce8e0cb8a6bb06f75d9bdad59b83006c92683bd73ced84a18223dde21fa81` | 未定義 |
| Protocol | `mc-remote/protocol/test/fixtures/block-value-v22.json` | 3,217 | `e8e108d59c40751d67a432543d75cb4bf9146ef9781721012085c80545b854f3` | 未定義 |
| Protocol | `mc-remote/protocol/test/fixtures/dimensions-v22.json` | 766 | `44993cce8d42fc8db15822788a2b6707971b5438edfb4eb77d774aad437c0628` | 未定義 |
| Protocol | `mc-remote/protocol/test/fixtures/direction-lightning-v23.1.json` | 20,367 | `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce` | 93 |
| Protocol | `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json` | 36,481 | `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2` | 111 |
| Protocol | `mc-remote/protocol/test/fixtures/events-v23.json` | 2,112 | `31760d267f3c2641042fbe8595fda9c259134a1c05423271a99cb74da1efa9aa` | 未定義 |
| Protocol | `mc-remote/protocol/test/fixtures/sign-v23.json` | 5,043 | `7ffb63c264602cba56117eefff1f9604b955df04c5cc655e877772b8ff7cd30e` | 7 group（B6-S01〜S07） |
| Protocol | `mc-remote/protocol/test/fixtures/spawn-v22.json` | 682 | `1120e6c8d41b05b65c916fa96f496b02884123ec7ef59b0a226eea48bebf3abd` | 未定義 |

## consumerと構造の補足

consumerは同じ公開source内で実際にfixtureを読み込むtest file。以下の行番号もそのsourceの値。

### one-shot-transport-v1.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"sample_payload": 1, "sample_message": 1}`。
- consumer: [mc-remote/bridge/test/server.test.ts:9](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/bridge/test/server.test.ts#L9)
- consumer: [mc-remote/bridge/test/transport.test.ts:12](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/bridge/test/transport.test.ts#L12)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:15](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L15)

### display-alias-v1.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"words": 16, "example": 1}`。
- consumer: [mc-remote/live/test/display-alias.test.ts:13](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/display-alias.test.ts#L13)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:14](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L14)

### observer-session-lifecycle.ndjson

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"ndjson_records": 2}`。
- consumer: [mc-remote/live/test/session.test.ts:14](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/session.test.ts#L14)
- consumer: [mc-remote/live/test/station-adapter.test.ts:8](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/station-adapter.test.ts#L8)

### scratch-main-lifecycle.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"snapshots": 2}`。
- consumer: [mc-remote/live/test/client.test.ts:11](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/client.test.ts#L11)
- consumer: [mc-remote/live/test/observer.test.ts:6](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/observer.test.ts#L6)
- consumer: [mc-remote/live/test/session.test.ts:13](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/session.test.ts#L13)
- consumer: [mc-remote/live/test/sound-resource-observer.test.ts:12](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/sound-resource-observer.test.ts#L12)

### station-attach-v1.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"attach_errors": 7, "bootstrap_ready_examples": 1, "bootstrap_not_ready_examples": 1}`。
- consumer: [mc-remote/live/test/station-adapter.test.ts:7](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/station-adapter.test.ts#L7)
- consumer: [mc-remote/live/test/station.test.ts:21](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/station.test.ts#L21)

### block-value-v22.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"state_text": 5, "invalid_state_text": 6, "block_value": 2, "error_text.malformed": 3}`。
- consumer: [packages/scratch-vm/test/unit/mcremote_block_value.js:2](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/mcremote_block_value.js#L2)

### dimensions-v22.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"accepted_refs": 4, "not_aliases": 4, "invalid_refs": 7}`。
- consumer: [mc-remote/live/test/observer.test.ts:10](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/observer.test.ts#L10)
- consumer: [mc-remote/protocol/test/contract.test.ts:44](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/protocol/test/contract.test.ts#L44)
- consumer: [packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js:6](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js#L6)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:17](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L17)

### direction-lightning-v23.1.json

- case数の意味: 明示B7 case ID。
- 構造の件数: `{"by_id_prefix": {"A": 16, "D": 31, "H": 8, "L": 32, "P": 6}}`。
- consumer: [mc-remote/live/test/observer.test.ts:13](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/observer.test.ts#L13)
- consumer: [mc-remote/protocol/test/contract.test.ts:45](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/protocol/test/contract.test.ts#L45)
- consumer: [packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js:8](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js#L8)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:20](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L20)

### entity-particle-v23.2.json

- case数の意味: 明示B8 case ID。
- 構造の件数: `{"nearby.cases": 19, "nearby.handle_transaction_cases": 7, "entity_lifecycle.cases": 7, "particle_stage_2.cases": 26, "sound.cases": 37, "resource_ids.cases": 15}`。
- consumer: [mc-remote/live/test/observer.test.ts:16](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/observer.test.ts#L16)
- consumer: [mc-remote/live/test/sound-resource-observer.test.ts:5](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/sound-resource-observer.test.ts#L5)
- consumer: [mc-remote/protocol/test/b8-owner-fixture.test.ts:14](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/protocol/test/b8-owner-fixture.test.ts#L14)
- consumer: [mc-remote/protocol/test/sound-resource-owner-fixture.test.ts:4](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/protocol/test/sound-resource-owner-fixture.test.ts#L4)
- consumer: [packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js:9](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js#L9)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:6](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L6)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:23](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L23)

### events-v23.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"poll_requests.rejected": 7, "poll_result.events": 3}`。
- consumer: [mc-remote/live/test/observer.test.ts:7](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/observer.test.ts#L7)
- consumer: [mc-remote/live/test/session.test.ts:15](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/session.test.ts#L15)
- consumer: [mc-remote/protocol/test/contract.test.ts:46](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/protocol/test/contract.test.ts#L46)
- consumer: [packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js:5](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js#L5)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:16](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L16)
- consumer: [packages/scratch-vm/test/unit/mcremote_event.js:2](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/mcremote_event.js#L2)

### sign-v23.json

- case数の意味: B6-S01〜S07のcase group（group内に複数入力あり）。
- 構造の件数: `{"case_group_ids": ["B6-S01", "B6-S02", "B6-S03", "B6-S04", "B6-S05", "B6-S06", "B6-S07"]}`。
- consumer: [mc-remote/protocol/test/contract.test.ts:47](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/protocol/test/contract.test.ts#L47)
- consumer: [packages/scratch-vm/test/unit/mcremote_sign.js:12](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/mcremote_sign.js#L12)

### spawn-v22.json

- case数の意味: fixture全体のcase数は未定義（sample／record数と区別）。
- 構造の件数: `{"spawn_particle_named_examples": 3, "spawn_entity_example": 1, "spawn_entity_legacy_example": 1}`。
- consumer: [mc-remote/live/test/observer.test.ts:8](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/live/test/observer.test.ts#L8)
- consumer: [mc-remote/protocol/test/contract.test.ts:48](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/mc-remote/protocol/test/contract.test.ts#L48)
- consumer: [packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js:7](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js#L7)
- consumer: [packages/scratch-vm/test/unit/extension_mcremote.js:24](https://github.com/Naohiro2g/scratch-editor/blob/691576f60b7f0824e1753bd6823901d01fbe2422/packages/scratch-vm/test/unit/extension_mcremote.js#L24)

## 依存と配布の境界

- VM runtimeは`@mc-remote/protocol`をimportせずwire定数をinlineで持つ。上記VM testがrepo相対pathでfixtureを直接読む。GUIのWireScope source testもrepo相対pathでProtocol fixtureを読む。
- Protocol owner testは同package内の相対pathで読む。`block-value-v22.json`を直接読むconsumerはVMのBlockValue testで、Protocol package内にこのファイルの直接readerはない。
- WireScope testはProtocol fixtureと自身のobserver／session／station fixtureを読む。WireScope／Bridge「専用」はfixtureの所有分類であり、専用fixtureの一部をVM testも読む。
- Bridge runtimeはpayload透過のtransportでProtocol packageをimportせず、Bridge testはone-shot transport fixtureを読む。
- `spawn-v22.json`の`spawn_entity.result`は歴史的な`mceh_` prefixの例。現行23.2のhandle合格値には使わない。Protocol contract testはparamsだけを利用し、現行handle例をevents fixtureから取得する。
- release manifestの`wirescope`はbrowser app ZIP、`wirescope-manifest`はdetached manifest、`contracts`はScratch GUIの`contracts/` tar。**Protocol fixtureの配布tarではない。**
- 横断consumerについて、参照したknowledge gateにはMcRemote／Pythonが111 case版B8 fixtureを取り込んだ記録がある。移管計画にはJavaもScratch owner由来のfixtureを読むとあるが、Javaはb8／b9の対象外で初回stable後に追従する。これらはSSOTの記録であり、本票の直接reader採取とは区別する。
- McRemote／Python／Java repo内のcopy、reader、取得経路は今回調査していない。これは公開Scratch sourceのowner／repo内consumer一覧であり、他repoの移管可否や適合を主張しない。
- 本票は移管の入力。topology、owner、source、distributionの変更は実施していない。

再採取: repo rootで`python3 handoff-materials/2026-10-03-b8-close-inventory/materials/collect-inventory.py`。
機械可読値: `materials/fixture-inventory.json`。製品fixtureの編集、build、live試験は今回行っていない。
