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
`connection_enabled`、`release_identity` の 5 項目である。
設計済みの `deploymentProfile`、capabilities の `minecraftConnection`、`notices` は未実装。
拡張内部の `_open()` guard は WebSocket 生成と token 読出しより前にあり、迂回経路は確認されていない。

fail-open を塞ぐ方法は未確定で、実装前に次のどちらかを選ぶ。

- Pages 配布物から runtime config を適用しない 4 entry を除く。
- VM 既定を disabled に倒し、consumer に明示的な有効化を要求する。

前者は Pages 配布境界、後者は VM 単体 consumer を含む公開 API 契約へ影響する。
「runtime config があるから成立済み」「4 entry は使われないから無害」は採らない。

### 2.2 UI スライス

`2026-07-12-06` を正本として次を実装する。

- 接続先設定を暫定 top-bar menu から Settings → Minecraft Remote へ収容する。
- パレットの信号機下へ設定先、実接続先、再接続要否を常時表示する。
- Scratch の Color Mode `original` / `high-contrast` へ追従し、状態を色だけで示さない。
- Scratch ロゴ左上の黒枠付き `▶` から開く、workspace を reflow しないお知らせ overlay を置く。
- overlay は reload 時に必ず開き、閉状態を `localStorage` や cookie へ保存しない。

状態の VM→GUI 経路は `2026-07-06-01` / `2026-07-06-02` の runtime EventEmitter を使い、
consumer と同時に配線する。`PERIPHERAL_*` 流用や独自 `postMessage` / `CustomEvent` 経路は増やさない。

### 2.3 b3 検収

検収基準の正本は knowledge 側の `2026-07-08-03` とする。dev repo の `AGENTS.md` は実行入口であり、
scope 別の品質基準を別正本として持たない。

- 全体 lint: exit code 0、error なし。upstream 既存 warning と今回変更起因 warning を分けて報告する。
- McRemote scope lint: warning なし。
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
