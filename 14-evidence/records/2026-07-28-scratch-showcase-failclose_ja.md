# Scratch showcase 二重 guard fail-close evidence

## Record

- test ID: `2026-07-28-scratch-showcase-failclose`
- test class: `unit/deterministic` + `live-auto` + `live-human`
- result: PASS（`build:dev` 成果物、下記 Claim boundary の範囲）
- observed at: 2026-07-28
- source repository: `Naohiro2g/scratch-editor`
- source branch: `agent/b3-pages-showcase-failclose`
- source commit: `b4647e1b77978273e4f5204d126e53c76d51116b`
- knowledge contract: `2026-07-28-01` / `2026-07-12-06` / `2026-07-27-03`

秘密実値は含まない（localhost 配信、token 未生成）。sanitized な counts と URL 応答表のみを収録する。

## Subject

`2026-07-12-06` が要求する二重 guard のうち、`2026-07-27-03` で実装済みだった runtime capability
guard（Pages artifact allowlist）に加え、build 時の接続コード無効化を実装した。

- build 時: `MCREMOTE_SHOWCASE` を scratch-gui の DefinePlugin で定数化し、`render-gui.jsx` が
  `vm.disableMcRemoteConnection()` を呼ぶ。ラッチは一方向で、後から読み込む runtime config は
  解除できない。
- runtime: 既存の `connection_enabled` を維持する。
- 拒否理由: 接続無効時の理由を全経路で `connection_disabled` に統一し、socket 未生成のブロックが
  「not connected to bridge」を返していた表示不整合を解消した。

## Scope items and claims

| Scope item / claim | Constraint | Observation | Result |
| --- | --- | --- | --- |
| VM unit | `extension_mcremote.js` | 45 tests / 131 assertions（新規 5 件は先に失敗を確認） | PASS |
| scratch-gui unit | `npm run test:unit --workspace=@scratch/scratch-gui` | 54 suites / 346 passed・1 skipped | PASS |
| lint | 両 package、変更行範囲 | exit 0・error 0、新規 warning ゼロ（`eslint -f json` で行番号照合） | PASS |
| bundle 比較 | showcase build vs 通常 build の `gui.js` | showcase 側のみ `vm.disableMcRemoteConnection()` 呼び出しを含む。両方とも `MCREMOTE_SHOWCASE` 文字列は残らない | PASS |
| live-auto | showcase build + `2026-07-27-03` prune 適用成果物をローカル静的配信 | `/` と `/index.html` = 200。`player.html` / `standalone.html` / `blocks-only.html` / `compatibility-testing.html` / `player.js` = すべて 404 | PASS |
| live-human（敵対条件） | 同じ配信物で runtime config を `connection_enabled: true` のまま保持 | connect 実行で `{"message":"This page is a showcase with the Minecraft connection turned off.","reason":"connection_disabled"}`。bridge への WebSocket 接続なし。`mcremote.sessionToken.v1:*` の生成なし。ブロックは通常どおり表示（拒否は実行時のみ） | PASS |

## Method note

配信・操作した成果物は `build:dev`（`NODE_ENV` 未設定）である。CI の GitHub Pages workflow は
`NODE_ENV=production` 下でビルドするため、production 成果物そのものでの確認はまだ行っていない。
DefinePlugin による定数畳み込みと `disableMcRemoteConnection()` 呼び出しはビルド設定に依存する
経路のため、production ビルドでも同じ経路を通ることを再確認する評価は Pages 配布前の残タスクとして
`13-scratch-client/scratch-roadmap_ja.md` §2.1 に残す。

## Claim boundary

本 record が主張する範囲は次に限る。

- `Naohiro2g/scratch-editor` commit `b4647e1b77978273e4f5204d126e53c76d51116b` の `build:dev` 成果物
- 上表の unit / lint / bundle 比較 / live-auto / live-human の観測
- runtime config が敵対的に `connection_enabled: true` であっても、build 時ラッチが接続を拒否すること

次は未確認であり、本 record は主張しない。

- `NODE_ENV=production` でビルドした Pages 配布用成果物そのものでの同一観測
- `origin/develop` への merge 後の状態（`2026-07-27-03` 時点で未 merge・未 deploy）
- production Bridge との実接続試行（本検証は接続不能の確認のみ）
