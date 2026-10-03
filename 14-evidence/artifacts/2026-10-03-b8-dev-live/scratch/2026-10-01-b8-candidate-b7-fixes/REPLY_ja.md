## Release gate 確認票（Scratch更新分・2026-10-01）

> 2026-10-02更新票: `../2026-10-02-b8-candidate-local-fixes/REPLY_ja.md`。本票は旧candidateの記録。

- 対象 repo: Naohiro2g/scratch-editor
- 対象 branch/commit: `agent/b8-compatibility@df34849d2502a498a06c5fe07a91d03e925124eb`。push後にgit ls-remoteで一致確認。
- release / channel: 2320.0.0b8 candidate／protocol 23.2.0
- gate coordinator: knowledge担当session
- human release owner: プロジェクトオーナー
- current phase: B7是正3件を独立commit・pushし、新sourceから候補成果物を再生成した。
- contract maturity / required test tier: b8確定contract／今回unit・deterministic。横断実機試験は未実施。
- knowledge contract path: `00-hub/release-gate-notes_ja.md`のb8節と確認票、`13-scratch-client/scratch-roadmap_ja.md`。runtimeも読んだ。
- knowledge contract commit: `893cbfdbc5a480531d1a1ad7ae6f0fad8d36ef9f`（remote mainから取得して読んだ）。
- gate manifest identity: 未提示
- change cone: Scratch VMの観測履歴保持・server error識別、GUI案内とBlockly入力欄。Protocol、WireScope app、Bridge、contracts、lockfileには旧candidateから差分なし。
- reused PASS / rationale: VM／GUI lint・GUI i18n:srcは同じsource内容で既実行。今回、対象unitとWireScope test、VM／GUI／Bridge build、WireScope artifact生成を再実行。
- exact compatibility set / freeze status: 未凍結
- target deployment / profile / lock: 通常devではScratch／Bridgeを開発端末で動かす。今回は配置・接続していない。
- authorized next action: 更新candidateのcommit／push・成果物生成・identity返却。registry／Release assetへの掲載は不要との回答に従った。
- test class: unit/deterministic
- 実行した command / 手順: 素材MANIFESTにcommandを記録。VM拡張123 subtests／524 assertions、GUI対象4 suites／41 tests、WireScope13 files／142 tests PASS。VM／GUI／Bridge build、WireScope build:artifact、diff check PASS。
- 結果: 下記3件を採用。空poll50往復で有用履歴100件保持、server backpressureで接続維持と明示的再試行、入力欄のnative編集ショートカットを検証。

- 空pollの履歴保持: `76f9e7d6384064faeef294843d702afde3017f64`
- server backpressureの案内分離: `b407ca9cfb4c5d77701d3b379f0b1dd23e4cf6cf`
- 入力欄の編集ショートカット: `df34849d2502a498a06c5fe07a91d03e925124eb`

- fixture: `mc-remote/protocol/test/fixtures/entity-particle-v23.2.json`は`054a3af`版と同一。36,481 bytes／111 case／SHA-256 `ca636b4a2685ea67f24d8e7931e3d30a84e7cec872bb5c5d2eadd178cdac39f2`。fixture更新なし。
- artifact source commit: `df34849d2502a498a06c5fe07a91d03e925124eb`。WireScope detached manifest内のsource commitとZIP全6 assetのbytes／hashを照合。

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `scratch-image-inputs.tar.gz` | 152,885,920 | `2b3eda9a42c09f326b2139848322aa955fe19099a139cd6935c18c2d9e6be458` |
| `bridge-image-inputs.tar.gz` | 38,138 | `fd43f714c77d2bc184bf882460dfc05a1ce345dc6d4f5b52505a6a9d2850908f` |
| `wirescope-app.zip` | 83,746 | `4cb349894b71d61d7ca143d8362a5b79deb1810e1d7a9e31ad30e29bfe370a07` |
| `wirescope-app.manifest.json` | 2,321 | `45d56d5012c2c0b21631597e160363d93bcf3e736b74cc0b8a1041afc8101413` |
| `contracts.tar.gz` | 1,908 | `48948ba47d55409f02a8ff8e0d44021b07859e11ffa5ca0f8598e6ef06082390` |

- WireScope ZIPは旧candidateと同一。manifestはsource commitの更新によりhashが変わった。Pythonの再生成入力は上記source commit。
- evidence record / artifact: ローカル素材`handoff-materials/2026-10-01-b8-candidate-b7-fixes/`。正式knowledge evidenceではない。GUI／Bridge tarはimage入力でありOCIではない。
- 未検証の境界: 実pluginとの横断接続、2-player receiver、描画・音・定位、実token再接続、統一real-browser試験。統一実施票を凍結後に受け取る。
- security / compatibility / rollback の確認: wireとfixtureは不変。shared環境、credential、world、configを変更していない。rollback実機確認は未実施。
- 判定を求める事項: 追加なし。更新candidate identityを返す。横断gateの最終判定は行わない。
- 着地確認: サウンドの高さ入力規則が同knowledge commitのScratch roadmapにあることを確認した（数字→pitch、N0〜N24→note、音名換算はユーザーコード）。
