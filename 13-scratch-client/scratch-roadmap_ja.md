# Scratch クライアント現行ロードマップ

> Scratch の現在地、直近 release scope、後続の作業束を置く現行 SSOT。
> 原点と経緯は [scratch-plan_ja.md](scratch-plan_ja.md) に完全保存するが、現行 scope は本書と
> [DECISIONS](../00-hub/DECISIONS_ja.md) から決める。

## 1. 現在地

現在は **R2 完了・R3 入口**。直近の同期 release 列は b3 とする。

b3 の確定範囲は次の二つだけとする。

1. GitHub Pages の接続無効 showcase profile
2. UI スライス（Settings 接続先、パレット状態表示、Color Mode、お知らせ overlay）

旧 `.sb3` の load / save 互換は、shadow block を top-level にしない修正
`5fb564d45b` と VM state snapshot integration test で解決済みのため b3 に含めない。
ただし、接続先と token は作品へ保存せずブラウザ実行環境へ属するという
`2026-07-08-01` の層分離と serialization regression は維持する。
`2026-07-10-01` は b2 から b3 へ送った当時の release gate 履歴として読む。

## 2. b3 scope

### 2.1 Showcase profile

`2026-07-12-06`、`2026-07-12-01`、`2026-07-14-04` を正本とし、次を満たす。

- UI と blocks は通常版と同じものを見せる。
- build 時と runtime capability の二重 guard で Minecraft 接続を無効化する。
- token 読出しと WebSocket 生成より前の共通 guard で拒否する。
- 拒否時は単なる未接続ではなく、展示版のため無効であることを説明する。
- Pages deploy / cleanup は operator の明示的な `workflow_dispatch` に限る。
- 公開される全 HTML entry が fail-close であることを確認するまで配布しない。

#### 現行実装との差分

`Naohiro2g/scratch-editor` commit `6212a34807` の source 読解では、build は
`index.html`、`player.html`、`standalone.html`、`blocks-only.html`、
`compatibility-testing.html` の 5 entry を出力し、Pages は build directory 全体を公開する。
runtime config を VM へ適用するのは `index.html` の経路だけで、残る 4 entry は適用しない。
GUI・VM・McRemote 拡張の既定は `connectionEnabled: true` で、拡張は builtin のため、
現行 build は残る 4 entry から production Bridge へ接続し得る。showcase profile は未成立である。

現行 runtime config schema は `bridge_url`、`default_sandbox`、`connection_targets`、
`connection_enabled`、`release_identity`、`notices` の 6 項目である。`notices` の wire schema
（`{heading, body, link?: {href, label}}` の配列）と showcase/container の挙動分岐は
`2026-07-31-01` で確定・実装済み（§2.2）。設計済みの `deploymentProfile`、capabilities の
`minecraftConnection` は未実装。
拡張内部の `_open()` guard は WebSocket 生成と token 読出しより前にあり、迂回経路は確認されていない。

`connection_targets` の schema と Bridge 共有の単位は `2026-07-30-03` で確定した。
`connection_targets` は `{id, label, sandbox}` の配列で、`label` は mc-remote-stack 側の
operator input（`role="connection-targets"`）が用意する表示用完成品であり、Scratch 側は
`label`/`sandbox` をそのまま表示・接続するだけで翻訳・解釈ロジックを持たない。同一配列内の
全 entry は単一の `bridge_url` を共有し、per-entry `bridge_url` は持たせない（Bridge を跨ぐ
比較・切替が要る場合だけ複数 entry を使う。それ以外は各環境が独立した Bridge・単一接続先を持つ）。

公開 entry が runtime guard を迂回する fail-open は `2026-07-27-03` の Pages 配布境界で塞ぐ。
全 entry document と bundle 名の分類表、公開可能 entry の allowlist を分け、公開可能なのは
runtime config を適用する `index.html` だけとする。分類にない entry document が build に現れた場合は
workflow を失敗させ、黙って除外も公開もしない。既知の非公開 entry は document と対応 bundle を
Pages artifact から除く。通常の開発用 build は変えず、VM 既定の `connectionEnabled: true` も変更しない。

scratch-editor の b3 candidate branch HEAD `6cf51e38624795cacfc532aacd055b34c8b9d869` には
`pages-artifact.mjs`、CLI wrapper、unit test、Pages workflow step の4 pathだけが実装されている。
unit 5件と新規3ファイルの lint warning-zero、scratch-gui 全体 lint の error-zero が PASSし、
実 build 複製への手動 CLI smoke も PASSした。
knowledge 側でも remote branch の commit と4 pathの同一差分を確認済みである。
ただし `origin/develop` へ未 merge・未 deploy なので、現行公開面が修正済みとは扱わない。
merge 後の build artifact inventory と全公開 URL の `live-auto` evidence を Pages 配布前に取得する。

この変更で runtime capability guard は全公開 entry に届く。

`2026-07-28-01` で `2026-07-12-06` が要求するもう一方の build 時の接続コード無効化も実装済みとなった。
`MCREMOTE_SHOWCASE` を scratch-gui の DefinePlugin で定数に畳み、`render-gui.jsx` が
`vm.disableMcRemoteConnection()` を呼ぶ一方向ラッチを追加し、後から読み込む runtime config では
解除できない。あわせて接続無効時の拒否理由を全経路で `connection_disabled` に統一した。
実装は `Naohiro2g/scratch-editor` commit `b4647e1b77978273e4f5204d126e53c76d51116b`
（branch `agent/b3-pages-showcase-failclose`）で、unit・lint は PASS、showcase build +
`2026-07-27-03` prune 適用成果物への live-auto（公開想定外 URL は全て 404）と live-human
（runtime config を敵対的に `connection_enabled: true` にしても接続拒否）を確認した。
`2026-07-27-02` matrix の showcase 項（公開される全 URL で接続不能）はこの二重 guard で満たす。

`2026-07-29-01` で production 成果物そのものでの再確認も完了した。showcase の runtime config を
追跡ファイルではなく Pages workflow が導出して配信する構成に変え、`connection_enabled: false` と
`release_identity`（公開対象 source の SHA）をビルド成果物側で確定させた。追跡ファイル
`packages/scratch-gui/static/mc-remote-runtime-config.json` はローカル開発既定のまま変更していない。
実装は `Naohiro2g/scratch-editor` PR #10 merge `18e061f344`・PR #11 merge
`c7087d7badd906f6bd5eb93776ec8fab0934d5ee` で `origin/develop` へ反映済み、Pages 公開済み。
`NODE_ENV=production` ローカルビルドと、pages.yml run `30387472889` による実際の公開面
（`https://naohiro2g.github.io/scratch-editor/`）の両方で、config が `connection_enabled: false`・
SHA stamp 済み、公開想定外の全 URL が 404 であることを確認した。
`2026-07-27-02` matrix の showcase 項は限定なしの PASS とする。
詳細と根拠は `14-evidence/records/2026-07-28-scratch-showcase-failclose_ja.md` を参照する。

VM 既定を disabled にする案は scratch-vm の public consumer 契約を変えるため b3 から park し、
consumer inventory を伴う専用の契約変更として起案された場合だけ再検討する。
「runtime config があるから成立済み」「4 entry は使われないから無害」は採らない。

### 2.2 UI スライス

`2026-07-12-06` を正本として次を実装する。

- 接続先設定を暫定 top-bar menu から Settings → Minecraft Remote へ収容する。
- パレットの信号機下へ設定先、実接続先、再接続要否を常時表示する。
- Scratch の Color Mode `original` / `high-contrast` へ追従し、状態を色だけで示さない。
- Scratch ロゴ左上の黒枠付き `▶` から開く、workspace を reflow しないお知らせ overlay を置く。
- overlay は reload 時に必ず開き、閉状態を `localStorage` や cookie へ保存しない。

お知らせ overlay は実装済みである（`2026-07-31-01`）。notices の wire schema は
`{heading, body, link?: {href, label}}` の配列（`link` 任意）で確定し、`src/lib/mcremote-runtime-config.js`
が正規化する。showcase（GitHub Pages）と container で挙動を分け、Pages 専用の変換 hook
`showcaseRuntimeConfig()`（`scripts/pages-artifact.mjs`）が設定済み `notices` の先頭に固定の
展示版免責 notice（`{heading: "Showcase build", body: "This page is a showcase with the
Minecraft connection turned off."}`）を追加する。container 配布はこの関数を経由しないため、
設定された notices がそのまま出る。実装は `Naohiro2g/scratch-editor` branch
`agent/b3-mcremote-player-pos-and-ui-slice` commit `f639a7283e`（新規
`packages/scratch-gui/src/components/notice-overlay/*`、`menu-bar.jsx`/`menu-bar.css`、
`mcremote-runtime-config.js`、`mcremote-l10n.js`、`scripts/pages-artifact.mjs`）。
unit 31件 PASS・lint error ゼロ・live-auto でお知らせ2件のスタック表示を確認したが、
実機（container）検証は未実施。container 側の notices 注入機構（operator input 経由の設計）は
`connection_targets`（`2026-07-30-03`）と異なりまだ無く、範囲外として明確に分離している。

状態の VM→GUI 経路は `2026-07-06-01` / `2026-07-06-02` の runtime EventEmitter を使い、
consumer と同時に配線する。`PERIPHERAL_*` 流用や独自 `postMessage` / `CustomEvent` 経路は増やさない。

Settings → Minecraft Remote の接続先選択は `connection_targets` の `label` をそのまま一覧表示し、
選択すると対応する `sandbox` へ接続する（§2.1、`2026-07-30-03`）。scratch-editor 側はこの schema を
実装済みである（`2026-07-31-02`）：`mcremote-runtime-config.js` の `normalizeConnectionTargets` が
`label` を必須フィールドとして fail-close 検証し、旧固定5種（stable/beta/alpha/dev/sandbox）の
react-intl 翻訳テーブルを削除して JSON 側の `label` をそのまま pass-through する。実装は
`Naohiro2g/scratch-editor` branch `agent/b3-mcremote-player-pos-and-ui-slice` commit
`4866448e25`。unit 55 suites/369件 PASS、lint error ゼロ、実機ブラウザで表示・選択・接続動作を
確認済み。mc-remote-stack 側（`render.py` の `_runtime_config()` への `connection_targets` 出力）は
引き続き未着手で独立。起動時 URL から接続先を制御する
実装を入れる場合は `connection_targets` 内の `id` 選択に限定し（例：`?connect=<id>`）、
`bridge_url` / `sandbox` を URL から自由に上書きする経路は公開 Scratch に作らない
（pairing/token 奪取の phishing リスク）。開発者個人用途の切替は既存の container 起動時
`mc-remote-runtime-config.json` 差し替えで足り、この用途に URL 上書きを追加しない。

### 2.3 b3 検収

検収基準の正本は knowledge 側の `2026-07-08-03` とする。dev repo の `AGENTS.md` は実行入口であり、
scope 別の品質基準を別正本として持たない。

- 全体 lint: exit code 0、error なし。upstream 既存 warning と今回変更起因 warning を分けて報告する。
- McRemote scope lint: warning なし。`2026-07-27-04` の `arrow-parens` 例外は
  `2026-07-27-05` で撤回済みであり、確認票で除外規則を設けない。
- deterministic: 生成 HTML inventory、全公開 entry の fail-close、runtime config の正常・欠落・HTTP・schema
  failure、token 非読出し、WebSocket 非生成、展示版説明、`.sb3` serialization regression を確認する。
- live-human: 通常版で pair / token reconnect、接続先別 token、`permission_denied` 時の token 温存、
  設定先と実接続先の表示、WireScope / パレット状態を確認する。
- showcase: 公開される全 URL で接続不能を確認する。
- hosted surface を更新する場合: exact source / artifact identity、deploy smoke、rollback、再 deploy を確認する。

過去 public epoch の archive evidence は carry しない。b3 の release gate に使う `live-auto` /
`live-human` はこの matrix で取り直し、`14-evidence/` に新しい sanitized record と必要な artifact を残す。
archive の b2 record、artifact、test plan は正式根拠として参照しない。

## 3. b3 後の R3 作業束

### R3-A — catalog picker と state UX（設計確定・scope 未割当）

設計は `2026-08-02-07` で確定済み。**b3 scope へ自動追加しない**（§2 は `2026-07-27-01` のまま）。実装をどの段へ置くかは別途判断する。

- picker は入力支援であり、結果は編集可能な文字列として既存入力欄へ入る。自由入力・変数・reporter を維持し、reporter を黙って取り外さない。
- vanilla block は短縮形（`oak_log`）、それ以外は完全修飾（`examplemod:ruby_block`）を入力する。Python 定数（`2026-08-02-05`）と同じ綴りにして、Scratch → Python 移行で二表記にしない。
- catalog は **hello の `catalogHash` と一致した後だけ** picker で使う。同梱既定版フォールバックは持たない。IndexedDB cache は再取得を省く保存であって、オフライン catalog ではない。
- 状態表示は `NOT ACQUIRED` / `CURRENT` / `UNAVAILABLE` の3つ。適合未確認の catalog を使わないので中間状態が生じない。
- 未接続時の通知は「最初の command 実行時だけ」。`connection_disabled` では接続を促さず展示版の説明を出す（`2026-07-28-01`）。
- `.sb3` へ保存するのは block 入力欄の文字列だけ（`2026-07-08-01`）。
- observation grant と display alias は別票。

### R3-B — 保存・学習・beta 体験

- 「ブラウザ保存作品」、匿名クラウド、`/project/<id>` を実装する（`2026-07-12-07`）。
- McRemote Tutorial / Debug 導線と、最初の 1 block までの教材を揃える。
- iPad / Safari を含む数分 onboarding と作例を R3 gate で確認する。

### R3-C — 運用 package と観測面

- backup 紹介、外部 transfer、restore 手順を同じ運用 package へ追加し、world と credential を分離する。
- 認証前後の availability guard、運用 metric、正規 bulk build / TNT の load test を beta gate へ追加する。
- Scratch 内 WireScope をパレット状態＋折り畳み drawer＋payload 時だけ広幅の構成へ育てる。
- standalone WireScope は runtime config の URL から秘密なしで開く。token を URL へ入れない。
- Backpack は IndexedDB＋BroadcastChannel の小さな検索 / pin 棚から始める（`2026-07-12-07`）。

per-sprite 第 4 tab は stream が実在するまで park する。main stream / substream と Scratch object の写像は
`2026-07-21-07` の b4 scope freeze 前設計 gate で確定する。

## 4. 搬送と確認

b3 の確定搬送票は本書の §2 と該当 DECISIONS ID を参照し、凍結した原点文書を根拠にしない。
scratch-editor 側は実装・検証結果を source commit、test class、実行 command、evidence path 付きで戻す。
knowledge 側が検収して公開正本へ着地し、commit / push 後に着地確認票を発行する。
