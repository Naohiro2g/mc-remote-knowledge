# Scratch showcase 二重 guard fail-close evidence

## Record

- test ID: `2026-07-28-scratch-showcase-failclose`
- test class: `unit/deterministic` + `live-auto` + `live-human`
- result: PASS（初版＝`build:dev` 成果物、Addendum＝`NODE_ENV=production` 成果物と Pages 公開面。下記 Claim boundary の範囲）
- observed at: 2026-07-28（初版）/ 2026-07-29（Addendum）
- source repository: `Naohiro2g/scratch-editor`
- source branch/commit（初版）: `agent/b3-pages-showcase-failclose` / `b4647e1b77978273e4f5204d126e53c76d51116b`
- source branch/commit（Addendum）: `develop` / `c7087d7badd906f6bd5eb93776ec8fab0934d5ee`
- knowledge contract: `2026-07-28-01` / `2026-07-29-01` / `2026-07-12-06` / `2026-07-14-04` / `2026-07-27-03`

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
| VM unit | `extension_mcremote.js` | 45 tests / 131 assertions。新規 5 件のうち 4 件（`disableMcRemoteConnection turns the connection off for the life of the runtime` / `runtime config cannot re-enable a connection disabled at build time` / `connect on a disabled deployment opens no socket and reads no token` / `a disabled deployment is reported as disabled rather than as not connected`）は実装前に失敗することを確認。残り 1 件（`a disabled deployment still shows every block`）は無効化がブロック表示に影響しないことを確認する既存挙動の回帰テストで、実装前から PASS | PASS |
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

## Corrigendum（2026-07-28）

初版の VM unit 行は「新規 5 件は先に失敗を確認」と書いていたが不正確だった。着地確認の照合で、
新規 5 件のうち実装前に失敗していたのは 4 件のみで、残り 1 件（ブロック表示への非影響を確認する
既存挙動の回帰テスト）は実装前から PASS していたことが判明した。上表を訂正した。

## Claim boundary（初版・2026-07-28）

本 record 初版が主張した範囲は次に限る。

- `Naohiro2g/scratch-editor` commit `b4647e1b77978273e4f5204d126e53c76d51116b` の `build:dev` 成果物
- 上表の unit / lint / bundle 比較 / live-auto / live-human の観測
- runtime config が敵対的に `connection_enabled: true` であっても、build 時ラッチが接続を拒否すること

次は未確認であり、初版は主張しなかった。

- `NODE_ENV=production` でビルドした Pages 配布用成果物そのものでの同一観測
- `origin/develop` への merge 後の状態（`2026-07-27-03` 時点で未 merge・未 deploy）
- production Bridge との実接続試行（本検証は接続不能の確認のみ）

## Addendum（2026-07-29）— production 再確認と Pages 配布

`2026-07-29-01` として、上記 Method note の残タスク（`NODE_ENV=production` 成果物そのものでの
再確認）と Claim boundary の未確認事項を解消した。

### Subject の変更点

showcase の runtime config は追跡ファイル `packages/scratch-gui/static/mc-remote-runtime-config.json`
ではなく、Pages workflow がビルド成果物から導出して配信する構成へ変えた。導出した config は
`connection_enabled: false` を確定させ、`release_identity` に公開対象 source の SHA（`github.sha`）を
stamp する。追跡ファイルは接続有効のまま変更していない（ローカル開発・他配備経路の既定を維持）。
config 導出は `2026-07-27-03` の prune step とは別 step にし、CI 失敗時にどちらが壊れたか判別できる。

- 搬送元 repo: `Naohiro2g/scratch-editor`
- 搬送元 branch/commit: `develop` / `c7087d7badd906f6bd5eb93776ec8fab0934d5ee`
- PR: #10 merge `18e061f344`、PR #11 merge `c7087d7badd906f6bd5eb93776ec8fab0934d5ee`。`origin/develop` へ反映済み、Pages 公開済み

### 追加観測

| Scope item / claim | Constraint | Observation | Result |
| --- | --- | --- | --- |
| unit | `prune-pages-artifact.test.js` | 9 tests PASS（新規4件は実装前に失敗を確認） | PASS |
| lint | `scripts/` / `test/unit/scripts/` | eslint 指摘ゼロ | PASS |
| CI | PR #11 | Build / Test scratch-gui / Test scratch-vm / Test Results / commitlint すべて pass | PASS |
| live-auto（ローカル production） | `NODE_ENV=production MCREMOTE_SHOWCASE=true` ビルド＋両 step 適用 | config が `connection_enabled: false`＋SHA stamp。minified バンドルで `disableMcRemoteConnection()` が無条件呼び出し（分岐ごと畳まれた） | PASS |
| live-auto（公開面） | pages.yml run `30387472889`（`develop` @ `c7087d7bad`、2026-07-28T18:26:58Z 起動、Build Editor / Deploy to GitHub Pages とも success） | `https://naohiro2g.github.io/scratch-editor/` の公開 config が `connection_enabled: false` / `release_identity: c7087d7badd906f6bd5eb93776ec8fab0934d5ee`。`/` と `/index.html` が 200。`player.html` / `standalone.html` / `blocks-only.html` / `compatibility-testing.html` / `player.js` / `guistandalone.js` が全て 404。公開バンドルの呼び出し箇所はローカル production ビルドと同一並び（`Nz=e=>{e.disableMcRemoteConnection(),e.setMcRemoteRuntimeConfig(...)}`）。`MCREMOTE_SHOWCASE` 文字列は残らず、展示版メッセージはバンドル内に存在 | PASS |
| live-human | 公開 URL をブラウザで確認 | OK | PASS |

秘密実値なし（公開 URL・token 未生成）。

### Claim boundary（更新後）

上記 Addendum により、初版が「次は未確認」としていた3項目はいずれも解消した。

- `NODE_ENV=production` でビルドした Pages 配布用成果物そのものでの同一観測 → 解消（ローカル production ビルドと公開面の両方で確認）
- `origin/develop` への merge 後の状態 → 解消（PR #10 / #11 とも merge・Pages 公開済み）
- production Bridge との実接続試行 → 未確認のまま（本検証は接続不能の確認のみで、これは意図した scope）

本 record（初版＋Addendum）が主張する範囲は、`Naohiro2g/scratch-editor` commit
`b4647e1b77978273e4f5204d126e53c76d51116b`（build:dev 検証）と `c7087d7badd906f6bd5eb93776ec8fab0934d5ee`
（production 検証・Pages 公開）の両方における、上表すべての観測に限る。production Bridge との実接続
試行は検証対象外のまま。
