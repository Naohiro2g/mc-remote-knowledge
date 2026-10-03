# B8 Scratchブロック実装と次回再開

## 実装したsurface

| opcode | 形 | 動作 |
| --- | --- | --- |
| `getNearbyEntities` | command | `[x,y,z,radius,max_entities]`を送り、選択リストへ各`{handle,type,pos}`のsnapshotを格納。0件はリストを空にし、失敗時は旧内容を保持 |
| `entityInfo` | reporter | nearby snapshotのhandle／type／x／y／zをネットワークなしで取得 |
| `getEntityPose` | reporter、monitor無効 | `[handle]`でpose snapshotを一度取得 |
| `entityPoseInfo` | reporter | poseのdimension／x／y／z／yaw／pitchをネットワークなしで取得 |
| `setEntityPose` | command | `[handle,dimension,x,y,z,yaw,pitch]`の応答を待ち、再読取りposeを検証 |
| `removeEntity` | command | `[handle]`の応答を待ち、成功時nullを検証 |
| `particleSpec` | reporter | data不要particle IDとworld／self receiverを組み立てる |
| `dustParticleSpec` | reporter | dustのRGB整数0〜255、size 0.01〜4を組み立てる |
| `blockParticleSpec` | reporter | 既存BlockSpec／catalog対応StateTextを使ってblock dataを組み立てる |

既存`spawnParticle`は文字列IDを保ち、新reporterが返すobjectのテキストをParticleSpecへ変換する。既存force省略・明示falseと座標先行の9／10 paramsは維持する。constructorのErrorTextはIDへ変換して送らず、actionable errorへ返す。FASTでもentity pose／removeはrequestで応答を待つ。entity handleの有効性／runtime policyの判定はサーバーに委ねる。

nearby初期入力はradius 10／limit 16。wire contractを変更しないScratch surfaceの初期値である。snapshotのJSON表現は内部実装で、学習者は値を変数・リストへ保持してaccessorへ渡す。raw UUIDやcomma-separated valueは公開しない。

## 確定搬送票（局所surfaceのレビュー用）

- 搬送元 repo: scratch-editor
- 搬送元 surface: Codex
- 搬送元 branch/commit: `agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`＋未commit差分
- 作成日: 2026-09-30
- 種別: 局所決定
- 決定: 上表のScratch surfaceを実装案として追加。exact label／menu／形の人間による表示確認は未完了で、承認済みsurfaceとは扱わない。
- 理由: 既存block／sign情報の一度取得snapshot＋ローカルaccessor、一覧の選択リスト格納、spawnのhandle変数格納に合わせる。副作用を持つentity操作は応答で成功を確認する。
- 却下案: なし
- 影響: Scratch VMの追加9ブロック、既存particleのobject対応、ja／ja-Hira翻訳、README説明。wire、plugin、Bridge、既存fixture bytesは変更しない。
- 根拠/検証: knowledge `974ba19f396336c2c52d657ef1c14a2f0d04c793`のwire §5.8.3とScratch roadmapのsurface境界。失敗を再現した3テストから実装し、FAST／remote error等の1テストを追加。unit/deterministic結果は下票。
- 既に変更した実装/文書: 下票の変更ファイル。
- ナレッジ着地希望: 人間の表示確認後、`13-scratch-client/scratch-roadmap_ja.md`へScratch surfaceとして記録。wire変更や横断release判定の依頼ではない。
- 捕捉 cleanup: 本directoryを着地確認または後続担当への移管で分類する。
- 着地後の確認戻り先: このscratch-editor session。

## セッションクローズ票

- repo: scratch-editor
- surface: Codex
- branch/commit: `agent/b8-compatibility@5aaa9c59acc393cd0a0de5cb45a5e619a5e87abe`＋未commit差分
- 作業範囲: B8 Scratch entity／particleブロック実装、McRemote問い合わせへの回答。
- 今回やったこと: 9ブロックとja／ja-Hira追加、既存particle object対応、failure／FAST／snapshot test、README更新。GUIのB7固定version期待値とmockをB8へ更新。
- 変更ファイル: `packages/scratch-vm/src/extensions/scratch3_mcremote/index.js`、`packages/scratch-vm/test/unit/extension_mcremote.js`、`packages/scratch-gui/src/lib/mcremote-l10n.js`、`packages/scratch-gui/test/unit/components/notice-overlay.test.jsx`、`mc-remote/README.md`。
- 検証: `node packages/scratch-vm/test/unit/extension_mcremote.js` 116 subtests／457 assertions PASS。GUIのl10n／notice対象2 suites／17 tests PASS。VM package lint 0 errors（既存warningあり）、GUI変更ファイルlint PASS。VM buildとGUI build:dev PASS。VM i18n:src実行済み（翻訳sourceはgitignore）。extension conversion 102 assertions／BlockValue 37 assertionsもPASS。git diff --check PASS。
- 未完了: commit／push、ブラウザ表示確認とexact surfaceの人間承認、実McRemoteに接続したlive試験。
- 次に読むもの: 本素材、`materials/mcremote-reply_ja.md`、最新remote mainのdev runtimeとScratch roadmap／wire §5.8.3。
- 次の一手: ブラウザ操作の接続が使える環境で9ブロックのja／ja-Hira表示を確認し、人間のsurfaceレビューへ進む。
- 未着地の搬送物: 本surface案とMcRemote問い合わせ回答。外部送信していない。
- NOTES/DECISIONS: repo-local NOTESへ再開情報を追記。knowledgeへの書込みなし。
- 注意点: browser-clientが「privileged native pipe bridge is not available; browser-client is not trusted」で接続できず、ブラウザ検証を主張しない。GUI全体unitの初回実行は68 suites PASS、notice overlayのB7固定期待値2件がFAIL。その2件を修正後、該当suiteと翻訳suiteはPASS。全GUI suiteの再実行は行っていない。shared deploy／release GREENを主張しない。ユーザー所有の未追跡`.markdownlint.jsonc`は変更していない。
