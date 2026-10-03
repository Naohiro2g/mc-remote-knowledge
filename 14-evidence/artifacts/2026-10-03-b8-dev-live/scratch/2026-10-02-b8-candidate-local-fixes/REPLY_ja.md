## Release gate 確認票（Scratch更新分・2026-10-02）

- 対象 repo: Naohiro2g/scratch-editor
- 対象 branch/commit: `agent/b8-compatibility@691576f60b7f0824e1753bd6823901d01fbe2422`。GitHub APIのbranch refとHEADの一致を確認。
- release / channel: 2320.0.0b8 candidate／protocol 23.2.0
- gate coordinator: knowledge担当session
- human release owner: プロジェクトオーナー
- current phase: human ownerが確認したローカル修正4件をcommit／pushし、candidate成果物を更新。devの横断試験前。
- contract maturity / required test tier: b8確定contract／今回unit・deterministicと既存ローカル確認の再利用。正式横断実機試験は未実施。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`のb8節と確認票、`00-hub/b8-gate-work-instructions_ja.md`、`13-scratch-client/scratch-roadmap_ja.md`、`13-scratch-client/scratch-block-value-projection-design_ja.md` §3・4・6。runtimeも参照。
- knowledge contract commit: `49d5a59f50d357bfe7cd9c5401811a5e9e58eb59`（remote mainから実際に取得・参照）。
- gate manifest identity: 未提示
- change cone: GUI picker表示／default省略、Blockly zoom、カード画像・説明・表示名、VM BlockInfoText parserとcategory表示名。Protocol、全共有fixture、WireScope app、Bridge、contracts、lockfileは旧candidateから不変。
- reused PASS / rationale: GUI／VMはcommit直前の同一sourceでunit／対象lint／翻訳抽出／production buildと独立browser確認を実施。commit後の製品sourceはHEADと一致。GUI配布入力build/とVMのPASSを再利用し、今回BridgeとWireScope build:artifactを新HEADで再実行。詳細と初回localization失敗の修正・再試験はMANIFESTに記録。
- exact compatibility set / freeze status: 参照gateは未凍結。Scratch source更新をcoordinatorへ返す。他repoのsetを確定しない。
- target deployment / profile / lock: 通常devではScratch／Bridgeを開発端末で動かす。shared配置・接続は今回行っていない。
- authorized next action: human ownerのcommit／pushとcandidate更新指示、およびcoordinatorの成果物生成・identity返却指示。registry／Release assetへの掲載は不要。
- test class: unit/deterministic（素材と同一sourceの既存ローカルbrowser確認を再利用。正式live-humanではない）
- 実行した command / 手順: Bridge build、WireScope build:artifact、正規化tar生成、verify-artifacts.py、git diff check。各PASS。GUI／VM等の再利用結果はMANIFESTの対応表と保存logを参照。
- 結果: ローカル修正4件を採用。tar全入力とZIP全6 asset、source・dependency identity、B8 fixtureのbytes／case数／SHAを照合してPASS。

```text
691576f60b feat(gui): update mc-remote artwork and display names
d69c4bb12b fix(gui): preserve script position during workspace zoom
95156290ec fix(vm): accept unqualified block information IDs
12b65b12c9 fix(gui): simplify catalog picker default states
```

- fixture: `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`は`054a3af017f1abb8cc01cf85b3bc83181e648e19`版と同一。36,481 bytes／111 case／SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`。変更なし。
- artifact source commit: `691576f60b7f0824e1753bd6823901d01fbe2422`。GUI／VMは同一コードの直前buildを再利用、Bridge／WireScopeは新HEADで再生成。WireScope manifestのsource commitとinput identityを照合。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-image-inputs.tar.gz` | 138,375,344 | `c7318efdfb22076c2d40501a526d7ca16a121510f7685d875fff34cdc4404843` |
| `bridge-image-inputs.tar.gz` | 38,138 | `fd43f714c77d2bc184bf882460dfc05a1ce345dc6d4f5b52505a6a9d2850908f` |
| `wirescope-app.zip` | 83,746 | `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07` |
| `wirescope-app.manifest.json` | 2,321 | `6ea468f50d50b52722b8f34145743df86cebc60865fe0e827be5632c26b024d0` |
| `contracts.tar.gz` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |

- WireScope ZIP、Bridge tar、contracts tarは旧candidateとbyte一致。GUI tarとWireScope manifestは更新。Pythonの同梱WireScope再生成入力は上記source commit（他repoへの実行指示・作業はしていない）。
- evidence record / artifact: ローカル素材 `handoff-materials/2026-10-02-b8-candidate-local-fixes/`。正式knowledge evidenceではない。GUI／Bridge tarはOCIではない。
- 未検証の境界: devでの横断接続と残るlearner block実動作、2-player receiver、描画・音・定位、実tokenのupgrade再接続、統一real-browser WireScope試験。追加Node版VM起動smokeはjsdom stylesheet pathのENOENTで未解決（GUI経路と区別）。
- security / compatibility / rollback の確認: wire／fixture／lockfile不変。GUI配布configはschema_version 1、connection_enabled false。credential／world／shared設定の変更なし。rollback実機試験は未実施。
- 判定を求める事項: 更新source／artifact identityを次のexact setへ反映してほしい。pickerのdefault省略とBlockInfoText手入力受理の局所決定の着地は別紙 `DECISIONS-HANDOFF_ja.md` を参照。横断gateの最終判定は行わない。
