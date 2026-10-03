# B8 fixture移管の凍結後棚卸し

- 作成日: 2026-10-03
- source: `scratch-editor@691576f60b7f0824e1753bd6823901d01fbe2422`
- exact set: `b8-integrated-artifact-set-1`
- knowledge contract commit: `749ba60dc8c18938e50ce66b8e820aac4401c69e`
- knowledge contract path: `10-protocol/protocol-tooling-migration-plan_ja.md`、`00-hub/release-gate-notes_ja.md`の移管準備と凍結節
- 結果: Protocol 7、WireScope 4、Bridge 1の12ファイルを凍結Git sourceから採取。全digestは凍結前の2026-10-01棚卸しと一致。

| owner | fixture | bytes | SHA-256 | 明示case数 |
| --- | --- | ---: | --- | --- |
| Protocol | `block-value-v22.json` | 3,217 | `e8e108d59c40751d67a432543d75cb4bf9146ef9781721012085c80545b854f3` | 統一case配列なし |
| Protocol | `dimensions-v22.json` | 766 | `44993cce8d42fc8db15822788a2b6707971b5438edfb4eb77d774aad437c0628` | 統一case配列なし |
| Protocol | `direction-lightning-v23.1.json` | 20,367 | `586d24bf40136eec31f1827f23ef5b317f15100a17a635d7fe9f165e0af40dce` | 93 |
| Protocol | `entity-particle-v23.2.json` | 36,481 | `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2` | 111 |
| Protocol | `events-v23.json` | 2,112 | `31760d267f3c2641042fbe8595fda9c259134a1c05423271a99cb74da1efa9aa` | 統一case配列なし |
| Protocol | `sign-v23.json` | 5,043 | `7ffb63c264602cba56117eefff1f9604b955df04c5cc655e877772b8ff7cd30e` | 統一case配列なし |
| Protocol | `spawn-v22.json` | 682 | `1120e6c8d41b05b65c916fa96f496b02884123ec7ef59b0a226eea48bebf3abd` | 統一case配列なし |
| WireScope | `display-alias-v1.json` | 322 | `85c8159a8b74788c0cf978078094d23a3cdae83c0be5e9aa9552bb820c8389ca` | 統一case配列なし |
| WireScope | `observer-session-lifecycle.ndjson` | 2,691 | `4fb06188a97025248cf5deea3ff9e50578d08136f079428d9bbac86ca920680b` | 統一case配列なし |
| WireScope | `scratch-main-lifecycle.json` | 5,100 | `3fe467c4e91fcbc2ccdee56a298d46b1b9dd7a1b4c2dfd0e9504ac2e6f609e2d` | 統一case配列なし |
| WireScope | `station-attach-v1.json` | 2,437 | `b50ce8e0cb8a6bb06f75d9bdad59b83006c92683bd73ced84a18223dde21fa81` | 統一case配列なし |
| Bridge | `one-shot-transport-v1.json` | 517 | `018d8fc8201dc8bf5689c53549df7be62b78c7e1d07e553f60c869a9ebcf7ec5` | 統一case配列なし |

Protocol fixtureは `mc-remote/protocol/test/fixtures/`、WireScopeは `mc-remote/live/test/fixtures/`、Bridgeは `mc-remote/bridge/test/fixtures/` にある。case数はB7/B8の明示IDの数で、それ以外を配列要素の機械的合計でcase数としない。B8はnearby 19+7、entity 7、particle 26、sound 37、resource ID 15の111件。observer lifecycle NDJSONは2行だが、2 caseとは主張しない。

## 同じ凍結sourceのconsumer／依存

- Protocolはproduction dependencyなしのleaf package。
- VM、WireScope、Bridgeのruntime sourceを走査し、`@mc-remote/protocol`のimport／requireがないことを確認。VMはwire定数をinlineで持つ。
- VM unitはProtocolのblock-value／dimensions／direction-lightning／entity-particle／events／sign／spawn、WireScope display-alias、Bridge one-shot fixtureをrepo内相対pathで読む。
- GUI WireScope source unitはProtocol fixtureをrepo内相対pathでimportする。
- WireScope unitは自身のobserver／session fixtureとProtocolのshared fixtureを読む。Bridge unitは自身のone-shot transport fixtureを読む。
- frozen workflowのmanifest role `wirescope` はbrowser app ZIP、`wirescope-manifest` はdetached manifest、`contracts` はGUI contractsアーカイブ。Protocol fixtureはcontractsへ含まれない。
- fixture readerのexact pathと行は `materials/fixture-consumers.txt`、package依存・runtime import走査・release roleは `materials/dependency-snapshot.json`、fixture identityは `materials/fixture-inventory.json`。

## 再採取と境界

`python3 handoff-materials/2026-10-03-b8-scratch-live-gate/materials/prepare.py`で凍結source／artifactを照合し、fixtureを再採取した。ログはmaterials/preparation.log。実サーバへの接続はしない。

これはb9移管へ渡すrollback基線の棚卸しであり、owner cutoverではない。現owner、repo内path、package／artifact配布、consumer取得先を維持した。repository作成、source移動、owner／distribution変更、park中の外部repo操作は実施していない。b9のtopologyとexactな実行範囲は別途人間批准を受ける。
