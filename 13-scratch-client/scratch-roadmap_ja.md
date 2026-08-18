# Scratch クライアント現行ロードマップ

> Scratch の現在地、直近 release scope、後続の作業束を置く現行 SSOT。
> 原点と経緯は [scratch-plan_ja.md](scratch-plan_ja.md) に完全保存するが、現行 scope は本書と
> [DECISIONS](../00-hub/DECISIONS_ja.md) から決める。

## 1. 現在地

現在は **R2 完了・R3 入口**。b3 は `2026-08-07-01` により横断スコープ完了・release済みとして凍結し、次の開発列を b4 とする。b3の正式release記録は `00-hub/release-gate-notes_ja.md` と `14-evidence/records/2026-08-07-scratch-b3-release-gate_ja.md` が持つ。

b3 の確定範囲は次の二つだけだった。

1. GitHub Pages の接続無効 showcase profile
2. UI スライス（Settings 接続先、パレット状態表示、Color Mode、お知らせ overlay）

独立 WireScope は `2026-08-06-03` により b3 の完了条件へ追加しない方針だった。b3 releaseには
同梱せず、b3後の後続として扱う。将来のreleaseへ同梱するコードは通常の
build・lint・security・regression gate を免れない。

2026-08-07 時点で、`Naohiro2g/scratch-editor` の
`develop@f7cea1177670f1ab3988b1b96a08f9f74736aab9` と未 commit worktree に、Scratch read-only
参照実装の最初の縦切りがある。これは b3 release には含まれず、公開配信済みとも扱わない。
実装到達点と残 gate は §3「WireScope 実装ロードマップ」および `2026-08-06-03` の
2026-08-07 追記を正本とする。

旧 `.sb3` の load / save 互換は、shadow block を top-level にしない修正
`5fb564d45b` と VM state snapshot integration test で解決済みのため b3 に含めない。
ただし、接続先と token は作品へ保存せずブラウザ実行環境へ属するという
`2026-07-08-01` の層分離と serialization regression は維持する。
`2026-07-10-01` は b2 から b3 へ送った当時の release gate 履歴として読む。

## 2. b3 scope（release済み・凍結）

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

### b4 scope（確定・main stream 1件）

`2026-08-16-08`により、b4は次の三本へ固定した。

1. Scratch／Python両sourceと共通app／artifactによるWireScope初期版
2. Scratch Catalog Picker
3. `player.getPose`／`player.setPose`

WireScopeは各sourceのmain stream 1件を順に観察し、common appとのreal-browser E2Eとhome alphaを
completion gateに含める。substream、multi-stream、console、LAN／public station、schema v1.1、長期履歴は
b4へ含めない。observer schemaの`streams[]`等の前方互換は維持するが、main／substreamとScratch objectの
写像をb4の設計・実装gateにしない。

#### b4 home-alpha pre-auth transport correction（確定 `2026-08-17-01`）

認証強制時の`auth_required`直後に`auth.pairBegin`を送る経路は、plugin TCPのEOF観測だけに依存しない。
Scratch adapterは`auth.pairBegin`／`auth.pairPoll`に限り、Bridge向けone-shot transport hintとraw JSON-RPC
payloadを一つのWebSocket messageで原子的に送る。Bridgeはhintだけを処理し、JSON-RPC payloadを解析・変更せず、
pluginへhintを送らない。one-shotでは旧backend generationを破棄して新TCPへpayloadを一度だけ送り、最初の完全な
NDJSON responseを得た後に当該generationを無効化・closeしてからbrowserへ転送する。固定delay、EOF待ち、自動再送は
使わない。`hello`、credential管理method、通常commandは従来のpersistent transportを維持する。

この変更はScratch adapterとBridgeのexact compatibility setで検収し、旧新混在を許容しない。exact envelope、未知hintの
actionable error、one-shot中の有限queue、timeout時close・再送なし、response完成→generation無効化→browser転送の順序を
fixture／testで固定する。home-alphaでは`auth_required`直後0msの`pairBegin`、複数回の`pairPoll`、token付き再`hello`、
通常persistent commandまでを一巡する。hintはWireScope observer schema v1へJSON-RPC frameとして投影しない。

### R3-A — catalog picker と state UX（設計確定・b4）

設計は `2026-08-02-07` で確定済み。**b3 scope へ追加せず b4 へ送る**。
b3 の catalog 実装と実測を入力に、picker の見せ方、state UX、教材上の説明をさらに洗練してから収容する。

- picker は入力支援であり、結果は編集可能な文字列として既存入力欄へ入る。自由入力・変数・reporter を維持し、reporter を黙って取り外さない。
- vanilla block は短縮形（`oak_log`）、それ以外は完全修飾（`examplemod:ruby_block`）を入力する。Python 定数（`2026-08-02-05`）と同じ綴りにして、Scratch → Python 移行で二表記にしない。
- catalog は **hello の `catalogHash` と一致した後だけ** picker で使う。同梱既定版フォールバックは持たない。IndexedDB cache は再取得を省く保存であって、オフライン catalog ではない。
- 状態表示は `NOT ACQUIRED` / `CURRENT` / `UNAVAILABLE` の3つ。適合未確認の catalog を使わないので中間状態が生じない。
- 未接続時の通知は「最初の command 実行時だけ」。`connection_disabled` では接続を促さず展示版の説明を出す（`2026-07-28-01`）。
- `.sb3` へ保存するのは block 入力欄の文字列だけ（`2026-07-08-01`）。
- observation grant と display alias は別票。

### 保存・移送作業束（b5／b6配置確定・R配置は最終整理待ち）

現行の保存・移送モデルは
[Scratch作品の保存・移送設計](scratch-project-storage-transfer-design_ja.md) と
`2026-08-16-01`〜`2026-08-16-03`を正とする。匿名cloud、`/project/<id>`、一般UGC hosting、
`mc-remote-storage`、Backpackは現行計画から撤回した。

- 作品全体はブラウザ保存作品と`.sb3`、スプライトはブラウザ保存スプライトと`.sprite3`で扱う。
- ブラウザ保存は同一storage partition・Editor originに閉じ、Minecraft接続先へbindingしない。
- 対応McRemote Editor間のブロック移送はOS clipboardを使う方向とし、bundle contractはfixture前に推測実装しない。
- b5は`.sb3`／`.sprite3`互換fixture、IndexedDB共通基盤、ブラウザ保存作品、quota／破損／migration、ファイル保存への退避を閉じる。
- b6はb5基盤と`.sprite3` fixtureを再利用してブラウザ保存スプライトを追加し、新しい保存基盤を作らない。
- OS clipboardによるブロック移送と審査済み教材は独立trackとし、b5／b6へ自動追加しない。
- McRemote Tutorial / Debug 導線と、最初の1 blockまでの教材を揃える。
- iPad／Safariを含むonboardingと保存・移送の実測gateは、最終R整理で配置する。

### R3-C — 運用 package と観測面

- backup 紹介、外部 transfer、restore 手順を同じ運用 package へ追加し、world と credential を分離する。
- 認証前後の availability guard、運用 metric、正規 bulk build / TNT の load test を beta gate へ追加する。
- **Scratch 内 WireScope は接続・pairing の薄い面（mini）に絞る**（`2026-08-02-09` で `2026-07-12-07` を部分改訂）。McRemote block palette の状態領域へ置き、workspace を reflow せず、script 編集面や sprite 表示を覆わない。残すのは接続状態・pairing 進行（pair code・実行コマンド・待機・期限切れ・再試行案内）・設定先と実接続先・actionable error・display alias・独立 WireScope の起動導線。

#### WireScope 実装ロードマップ

正本は `2026-08-06-03` とし、独立 WireScope は共通の `@mc-remote/live` web app と
Scratch／Python それぞれの source adapter・launcher で構成する。別々の UI app は作らない。
observer schema は初版から `streams[]` を持ち、`1 stream = 1 connection = 1 build state` を維持する。
target と stream を同一 ID にせず、将来は target 配下へ main／substream を追加する。

##### Scratch read-only 参照実装の到達点（2026-08-07）

最初の縦切りは実装済みである。共通 `@mc-remote/live` app、
`schema=mcremote.observer`／`schema_version=1`／`streams[]` の observer contract、Scratch main
stream lifecycle fixture、Scratch の generation-side allowlist adapter、WireScope mini から別 origin
app を開く導線までを含む。handoff は送信元 window・exact origin・exact `targetOrigin` を検証し、
`MessageChannel` と15秒有効・一回限りの grant を使う。直接アクセスした WireScope は観測権限を持たず、
fail-closed の待機画面を表示する。

observer へ生成するのは sanitized hello、permissions、world constants と、allowlist 済みの
hello／建築／world／player frame・payload だけである。`auth.*`、token、pair code、player UUID、
credential／device 情報、無制限な frame 履歴や VM 内部状態は生成しない。grant、history、observer
session は `.sb3`／Web Storage へ永続化しない。

WireScope、Scratch／McRemote UI、McRemote extension blocks は `en`、`ja`（「日本語」）、
`ja-Hira`（「にほんご」）を持つ。`ja-Hira` は独立した正式 locale ID であり、大文字・小文字を
正規化した判定後も canonical ID `ja-Hira` を保持する。McRemote の学習者向け `ja-Hira` 文言には
漢字を含めず、固有名詞、接続先、入力値は原表記を維持する。

検証済みは、`@mc-remote/live` 3 test files／15 tests、lint／format、web app／library build、
scratch-gui 関連 5 suites／41 tests と変更範囲 lint、scratch-vm McRemote 関連 59 subtests／
172 assertions と webpack build、scratch-gui production build、静的な CSP meta・handoff message・
永続化 API 非使用・秘密情報非生成、実ブラウザーでの直接アクセス fail-closed と `ja-Hira` 表示である。

残る gate は、実 Scratch→Minecraft 接続から独立 WireScope までの完全 E2E、別 origin 配信で
CSP／COOP／cache／artifact identity を応答 header と deploy smoke で保証すること、Pythonの実artifact配布／
browser launcher／real-browser attach、multi-stream／multi-source、長期観察、将来console sourceである。
正式 evidence record は
実接続 E2E または deploy gate の実施時に作成する。

##### 共通session coreの実装具体化（2026-08-11）

`2026-08-11-02`に従い、Scratch adapterのselection windowを`2,000ms`として、15秒のgrant寿命とは
別定数へ分離した。openerは候補条件に留め、window内に有効なMessagePortを受理した時点でScratch adapterを
確定し、port受理後はstation adapterへfallbackしない。

session protocol v1の初期serialized shapeは
`mc-remote/live/test/fixtures/observer-session-lifecycle.ndjson`へ固定した。既存Scratch wireは履歴省略を
持たないためadapter内で`dropped_frames: 0`へ正規化し、`mcremote.observer` schema v1へhistory fieldを
追加しない。Python station adapterは同fixtureをconformance入力として利用できる。

当初搬送時点はScratch `develop@1cf1f02c6a6519b2edf3514a47481ad36d44a363`上の未commit worktreeだった。
その後、selection window、session fixture、artifact、station attachを
実装・artifact source `192d1e3ccd213fb5012b92655e51b779270e15be`へ固定し、PR #16のmerge commit
`27f8906170bec5146714358d7017dbd601504775`としてremote `develop`へ着地した。

##### Immutable artifact contractの実装具体化（2026-08-11）

`2026-08-11-02`に従い、共通appをdeterministicな`wirescope-app.zip`とdetached
`wirescope-app.manifest.json`として生成する。manifestはarchive hashと既決のsource／build／protocol／asset／
license identityを持つが、ZIPへ内包せず、自分自身のhashを内部へ持たない。Python wheelとStack lockはarchiveと
manifest双方を外側でpinし、manifest内archive hashとも照合する。runtime port／attach codeをimmutable assetへ
埋め込まない。

正式artifact生成はclean-checkout gateを必須とし、dirty worktreeから作った出力を正式identityとして配布しない。
当初搬送時点はScratch `develop@1cf1f02c6a6519b2edf3514a47481ad36d44a363`上の未commit worktreeだった。
generator、CLI、NOTICE、package scripts、protocol version constants、testsを含む固定参照は
`192d1e3ccd213fb5012b92655e51b779270e15be`である。同commitのclean checkoutから生成した
`wirescope-app.zip`のSHA-256は`947a6d478439ce60199be1b18b3c8d3cebdb46d2c022f8d9933138b23b2a5897`、
detached `wirescope-app.manifest.json`は
`4310ae34ec04997dbf136afa463a39de08ef97acc651f6fb70357b272ea1a143`である。同一入力からの2回生成、
全assetのbyte数／SHA-256照合がPASSした。これは正式配布済みという意味ではない。

##### Artifact delivery unitの固定（2026-08-12）

`2026-08-12-02`に従い、consumerへ渡す単位をcanonical filenameとbytesを変更しない
`wirescope-app.zip`／`wirescope-app.manifest.json`のexact 2-file pairへ固定した。wrapper archiveや第三の
generated lock fileは追加せず、受領distributionが両hashの外側pinとpackage inventory検証を所有する。
Python wheelは両fileを個別package dataとして`RECORD`で検証する。

Scratch実装は`agent/wirescope-artifact-delivery@09ccd563c93048f8a1d0a3dc1cee2d1f0ffb4681`で、clean source
`192d1e3ccd213fb5012b92655e51b779270e15be`からの再生成hash、ZIP integrity、AGPL `LICENSE`、NOTICE、
対応source導線、protocol compatibility setを確認した。`@mc-remote/live` 48 testsとbuildがPASSした。
Actions artifactや一時handoff directoryを公開配布正本とせず、公開channelはE2E／license gate後に判断する。

##### Station attach v1 fixtureの固定（2026-08-12）

`2026-08-12-01`に従い、station attach v1のbootstrap、attach request、error mapping、byte上限、
security header、NDJSON framingを、固定参照
`agent/wirescope-session-artifact@192d1e3ccd213fb5012b92655e51b779270e15be`の
`mc-remote/live/test/fixtures/station-attach-v1.json`へ固定した。fixture内容のSHA-256は
`b50ce8e0cb8a6bb06f75d9bdad59b83006c92683bd73ced84a18223dde21fa81`である。

Scratch browser adapterとPython loopback stationはこのfixtureを共通wire contractとして使い、client別shapeを
作らない。attach codeをURLへ置かず、responseを一括で無制限bufferへ保持せず、strict UTF-8／LFのNDJSONとして
逐次処理する。CR／CRLF、BOM、空line、未終端line、上限超過lineは拒否する。

Scratch側は47 tests、build、Scratch regression 3 testsがPASS。Pythonの機械的conformanceは
`Naohiro2g/minecraft-remote-api@14a662e173e3805870987691a938292a5de6e456`、実loopback HTTP stationは
`main@973c7f44211ad0fc2f87e1d119dcdbf04983a52f`へ固定した。Python wheel同梱とautomatic browser launcherは
`codex/wirescope-wheel-browser-e2e@8c2360abffe64d3d0b84e2a8b3e1c5da7d25d018`へ到達した。attach code
再発行trigger、実browser UIによる共通app／MessageChannel regression照合は未実装／未検証のまま維持する。

Scratch PR branchの既存CIではscratch-gui lint 2件が失敗したが、対象の
`packages/scratch-gui/test/unit/util/mcremote-wirescope-source.test.js`はPR差分に含まれない。今回の
session／artifact／station attach sliceの合格根拠には、この無関係な失敗を含めない。

##### 共通display alias contract v1（2026-08-12）

`2026-08-12-03`に従い、Scratchのalias生成語彙をsource横断の16語と
`WORD-WORD-NNNNNN`形式へ固定した。機械可読正本は
`develop@3b3d1f1c8a0dd66d265c5c6ea515cc5ac291209b`の
`mc-remote/live/test/fixtures/display-alias-v1.json`（SHA-256
`85c8159a8b74788c0cf978078094d23a3cdae83c0be5e9aa9552bb820c8389ca`）である。source実装commitは
`8678cfb44cd58275a76d7254297d32d147a67e71`である。

Scratchは60 tests／174 assertions、`@mc-remote/live` 9 files／48 tests、scratch-vm lint error-zero、buildが
PASSした。aliasは表示専用の非秘密情報で、`source_kind`、target／stream ID、attach／認可と分離する。
observer schema v1と既存lifecycle fixtureは変更していない。Pythonの現行8桁uppercase hex生成器は、共通fixture、
active衝突再生成、connection epoch lifecycleへの後続移行対象である。

##### 初期版の live-human 検収（2026-08-08）

Scratch 初期版は `Naohiro2g/scratch-editor`
`develop@1cf1f02c6a6519b2edf3514a47481ad36d44a363` で commit・push 済みとなり、schema v1 と
狭幅 read-only UI を初期版の合格点として受理した。protocol `21.0.0`／Minecraft `1.21.11` の
local environment を使う live-human E2E で、Scratch→Bridge→Minecraft→独立 WireScope の
`hello` と `chat.post` の request／response、同一 main stream の継続更新を確認した。Minecraft、
Scratch、WireScope を横並びにできる狭幅2 column UI と `ja-Hira` 表示も人間確認済みである。

schema v1 の `streams[].hello` は初期 handshake の記録であり、そこにある `world`／`origin` は
接続時の値として保持する。後続の `build.setWorld`／`build.setOrigin` を受けても `hello` を現在値で
上書きしない。現在の可変 build state は schema v1 の未宣言 field として追加せず、次の schema slice で
`current_build_state` と lifecycle／fixtureを共に定義する。現在値を得るためだけに Minecraft を25msごとに
pollingする方式も採らない。この分離により、Scratch／Python adapter は同じ handshake record と可変状態の
境界へ追従できる。

これにより、上記2026-08-07到達点の「完全 E2E」gapは、初期 main stream の `hello`／`chat.post` と
継続 snapshot の範囲で閉じた。残るのは公開配信の CSP／COOP／cache／artifact identity deploy gate、
Pythonの実artifact配布／launcher／real-browser attachとdeployment profile別の後続transport、実際の複数 connection を使う
multi-stream E2E、現在 build state の次 schema
slice である。正式根拠は
[2026-08-08 WireScope initial live-human record](../14-evidence/records/2026-08-08-wirescope-initial-live-human_ja.md)
を参照する。

1. **b3 前に計画した Scratch read-only 版（最初の縦切り実装済み・未配信）**
   - Scratch を先行参照実装とする。b3 blocker にはせず、b3 release には同梱しなかった。
   - observer schema、security allowlist、lifecycle fixture、Scratch adapter 契約を schema v1 として固定した。
   - 初版は Scratch の main stream 1件を観察し、別タブ／window で sanitized hello、permissions、world constants、frame／payloadを read-only 表示する。
   - runtime config の信頼済み URL、origin/source 検証、exact `targetOrigin`、`MessageChannel`、一回限り grant を使う。
   - `auth.*`、token、pair code、player UUID、credential 情報を独立 WireScope へ渡さない。
2. **b3 後：Python 追従**
   - Python API 担当は b3 release 後に着手し、Scratch が先行固定した schema、fixture、adapter 契約へ追従する。
   - Python adapter conformanceは合格済み。最初のstation実装はbrowser-loopback profileへ限定し、source process内のin-process stationとする（`2026-08-11-03`）。
   - 共通app、same-origin station attach、observer session envelope、artifact contractの正本は[station attach設計](../15-wirescope/wirescope-station-attach-design_ja.md)とする。
   - `wirescope=True`は`WireScopeStation.local()`のlow-floor省略形とし、cross-process、LAN、VPSへ意味を拡張しない。引数なし`mcremote wirescope`は予約のまま維持する。
   - Scratch app側はMessageChannel adapterとstation attach adapterを共通session coreから分離し、選択を状態機械とtestで固定する。
   - 初版は `Minecraft.create()` で成立した main stream 1件を観察する。
   - Scratch 後続前段と短期間だけ並走して両 adapter の conformance を確認し、長期間の共同設計状態にしない。
   - `2026-08-16-08`により、共通app／artifactとPython main streamのreal-browser E2Eはb4初期版の一部とする。
3. **後続前段：Scratch main／substream と長時間観察**
   - Scratch object model から main／substream への別途確定する写像に従い、各 stream を独立 connection・独立 build state として観察する。
   - observer session が開いている間の長時間観察を実装する。
   - observation history、grant、observer session は `.sb3`／`localStorage` へ永続化しない。
4. **後続中段：Python substream と複数 source**
   - Python の明示 substream API へ追従し、複数 source／複数 stream の read-only 観察、検索、比較を実装する。
   - source／target ごとの grant を分離する。
5. **後続後段：独立console sourceの予約**
   - browser observerへcontrol capabilityを付与せず、consoleを実装する場合は自前でpairingする独立sourceとして別streamを持たせる（`2026-08-10-03`）。
   - commandの認可、transport、target、教材gateは着手前に別途設計・批准する。openerの既存connectionを借りた代理送信を採らない。

`2026-08-02-09` のScratch read-only実装、grant、display alias、generation-side allowlistは維持する。
共通配置とPython transportの正本は
[WireScope deployment設計](../15-wirescope/wirescope-deployment-design_ja.md)、共通app attach／artifactとPython
初期profileは[station attach設計](../15-wirescope/wirescope-station-attach-design_ja.md)、長期ビジョンは
`2026-08-10-03`とする。別origin配信ではCSP／COOP、cache、artifact identity、deploy smokeを配信側のgateに
加える。

per-sprite 第 4 tab は stream が実在するまで park する。main stream／substreamとScratch objectの写像は
`2026-08-16-08`によりb4 scope freeze前gateから外し、post-b4の独立sliceで再開する。

### b5／b6 plugin APIのScratch投影

b5／b6の横断scopeはDECISIONS `2026-08-16-04`〜`07`と
[wire contract](../10-protocol/wire-format-design_ja.md) §5.4〜§5.8を正とする。Scratchはserverの
`events.poll`を利用者へ直接露出せず、connectionごとに一つのpollerからtype別hat blockへ投影する。

- mixed batchをFIFOでtype別hatへ振り分ける。
- event DTOは起動したScratch threadへ個別に束縛し、共有の「最後のevent」を作らない。
- overflow、capacity loss、明示破棄を確認可能にし、空batchや通常切断へ畳まない。
- disconnect時にpoller、cursor、thread context、event cache、entity handle cacheを回収する。
- event座標をworld blockへ渡す前に、eventがcaptureしたworld／originと現在値の一致を確認し、
  不一致をactionable errorにする。

`world.spawnEntity`のhandleは副作用と同じresponseから原子的に受け取る。共有の`last entity` reporterは
作らない。副作用reporterをmonitor不能にできるruntimeではreporterを優先し、保証できない場合は
出力変数付きcommand blockへ確定する。この選択はScratch runtimeのprototype結果を待つ。

monitor-driven reporterには、monitor評価のthrottle、同一引数のin-flight request coalescing、
disconnect時のcache破棄を設ける。明示的なscript callは毎回実行する。対象は
`world.getHeight`、b6のentity pose／nearby、queue metric等である。`world.getHeight`はoptional引数を
一つのblockへ押し込まず、maxYなし／ありの二reporterへ投影する。`height_not_found`を`-1`へ変換せず、
空文字＋actionable errorまたは別found状態のどちらにするかを実装前に固定する。

連続位置は小数第3位、yaw／pitchは小数第2位にpluginが正準化したwire numberを受け取る
（DECISIONS `2026-08-19-01`）。Scratch adapter／blockは値を再round、yawを再wrap、pitchをclampしない。
monitor等のUIが末尾ゼロを補っても、thread context、変数、WireScope frameの値を変更しない。set系blockは
入力を表示桁へ丸めず送信し、成功後のserver resultを正とする。integer fieldの小数入力を黙って整数化しない。

b5のWireScope schema v1.1対応はplugin fixture、Python observer projection、Scratch source adapter、
common app artifactと同じcompatibility setで行う。plugin wire conformanceと共通UI／real-browser E2Eは
別gateとし、Scratch側だけでallowlistやlegacy methodを拡張しない。

## 4. 搬送と確認

b3 の確定搬送票は本書の §2 と該当 DECISIONS ID を参照し、凍結した原点文書を根拠にしない。
scratch-editor 側は実装・検証結果を source commit、test class、実行 command、evidence path 付きで戻す。
knowledge 側が検収して公開正本へ着地し、commit / push 後に着地確認票を発行する。
