# マイクラリモコン Scratch対応 設計・開発計画

> **状態＝原点文書（完全保存）。現行 contract の正本ではない。**
> 本プロジェクト再始動の起点。1年ぶりの再始動にあたり、Scratch client を自前でゼロベースから作り、
> そのために新 protocol を設計し、plugin と Python client も刷新する、という動きはここから始まった。
> SSOT を経由せずに進めていた時期の作業文書であり、**内容は当時のまま保存して改訂しない**。
> 現行の contract は [wire-format-design](../10-protocol/wire-format-design_ja.md) と
> [versioning-design](../10-protocol/versioning-design_ja.md) が正本で、本文書と食い違う場合は
> そちらが優先する。収容の判断は DECISIONS `2026-07-26-01`。

> このドキュメントは、次回セッションの起点となる設計・計画のまとめ。
> 本計画は「マイクラリモコン」プロジェクトに Scratch クライアントを追加する作業に関するもの。

## 0. プロジェクト全体構成(概要)

「マイクラリモコン」は、Minecraft を外部からプログラムで操作してリモート建築などを行うための学習向けプロジェクト。8歳〜80歳を対象に、ビジュアル(Scratch)とテキスト(Python)の両方の入口を提供する。

### 公開サイト・ドメイン

- **`mc-remote.com`** — プロジェクトの拠点ドメイン(所有済み)。サブドメインを各サーバーに割り当てる。

### 主要リポジトリ

プロジェクトのリポジトリハブ:`github.mc-remote.com`(運営:Code2CreateClub)

| リポジトリ | 役割 |
| --- | --- |
| `github.com/Naohiro2g/McRemote` | PaperMC サーバー用プラグイン(Paper plugin)。PaperMC サーバーと並走し、クライアントが通信する専用サーバーを提供。Minecraft 側でリモコン操作を受ける本体。LuckPerms 連携・認証(pair / token)を担う。 |
| `github.com/Naohiro2g/minecraft-remote-api` | Python の API / クライアント。プラグインへ TCP 接続してリモコン操作を行う。ユーザー操作を仲介し、コード記述・自動建築を可能にする。 |
| `github.com/Naohiro2g/mc_remote_samples` | Python のサンプルコード(リモコン建築などのユーザーコード例)。 |
| `github.com/Naohiro2g/scratch-editor` | 本計画で新規に進める、McRemote 拡張入りの改造版 Scratch Editor(scratch-editor モノレポの fork)。 |

### サーバー / 構成要素

| 構成要素 | ドメイン / 接続先 | 役割 |
| --- | --- | --- |
| Scratch Editor(stable) | `scratch.mc-remote.com` | ブラウザで開く改造版 Scratch |
| Scratch Editor(dev) | `scratch-dev.mc-remote.com` | 追従・新機能テスト用 |
| Scratch Bridge | `bridge.mc-remote.com` | wss を受ける中継(1つに固定) |
| Sandbox(Minecraft + McRemote plugin) | `sb.mc-remote.com:25575` | リモコン操作の実行先。Python API もここに接続 |

### 前段階の経緯

- 本プロジェクトの前段階では、takecx への依頼で Forge mod 版の socket サーバーが動き、そこに接続していた。
- 現行は **PaperMC 用プラグイン(サーバー)+ Python API / クライアント**の組み合わせで運用中(socket = TCP 通信、複数クライアント対応済み)。
- 本計画は、ここに **Scratch クライアント**を追加するもの。takecx の各実装(scratch-vm / scratch-gui / RemoteControllerMod)は**参考のみ**で、ゼロベースで再構築する。

---

## 1. 基本構成と方針(概略)

マイクラリモコンに **Scratch によるビジュアルプログラミング** のクライアントを追加する。
既存の Python API / クライアントはそのまま併存させ、プラグイン(サーバー)側の改修は最小に留める。

### 全体の流れ

```text
[ブラウザ]
  Scratch Editor (scratch.mc-remote.com)
      │  wss://  (TLS, ブラウザ→bridge)
      ▼
  Scratch Bridge (bridge.mc-remote.com)   ← 1つに固定
      │  TCP 25575  (平文, サーバー間)
      ▼
  McRemote Plugin / Sandbox (sb.mc-remote.com:25575)
      ├─ 既存 Python クライアント (TCP, 変更なしで併存)
      ├─ bridge 経由 Scratch
      └─ (将来) WebSocket 直結クライアント
```

### 核となる設計判断

- **bridge 方式を採用**(localhost リレー方式は不採用)。ブラウザの混在コンテンツ制約は「HTTPS ページから平文 ws:// 外部接続は不可、wss:// なら可」。よって正規 TLS ドメインの bridge へ wss で繋げば、**全ブラウザ(Safari 含む)と iPad で追加ソフトなしに動く**。
- **プラグインは当面 TCP のまま**。bridge が wss ⇔ TCP を変換するため、プラグイン側の WebSocket 化を待たずに開発を始められる。プラグインから見れば bridge 経由の Scratch は Python クライアントと同等。
- **認証は token、認可は LuckPerms** に完全分離。token は「誰か」を証明し、「何ができるか」は毎回 UUID → LuckPerms で判定。admin token のような特権 token は作らない。
- **保存は三層**(ローカル自動保存・.sb3・匿名クラウド)。改造版 Scratch の弱点である「作品が保存できない」を補い、オープンソース志向に沿って公開・共有・リミックスを支える。

---

## bridge 実装（言語・配置・責務）

bridge の実装言語は **TypeScript（Node）**、配置は **scratch-editor モノレポ内**（DECISIONS `2026-06-27-06`）。

**責務（薄い透過プロキシ・protocol 意味論はパースしない）**：

- **フレーム詰め替え**＝wss 経路（ブラウザ）の WS 1メッセージ ⇔ 直 TCP 経路（plugin）の改行区切り1行（wire-format-design §2）。WS メッセージを compact 1行＋`\n` で TCP へ、TCP の行を WS メッセージへ。JSON 中身は不可触。
- **Origin 許可リスト**＝WS ハンドシェイクで stable（`scratch.mc-remote.com`）/dev（`scratch-dev.mc-remote.com`）のみ許可。
- **全二重・push 透過**＝非依頼の server→client push（デバッグ/observer、2026-06-24 横断）を request/response 結合やバッファリングなしに素通し。
- **TLS 非関与**＝Caddy が前段で終端（scratch-plan Phase 2）、bridge は localhost 平文 ws↔TCP。

**型共有（契約 leaf）**：wire 型＋定数（JSON-RPC エンベロープ・フラット hello・error object・catalogHash・method 名・`PROTOCOL_VERSION`・error reason）は 10-protocol(SSOT) のミラー **`@mc-remote/protocol`（何にも依存しない leaf）** に集約。**bridge と live（WireScope）が import**、**vm 拡張は inline 定数維持（import しない）**＝拡張は scratch-vm builtinExtensions に build-time bake されるため共有 import を持てず、runtime 互換は hello の `protocol` semver ネゴ（§8）が担う（共有 package は DX 用で互換の安全網ではない）。DECISIONS `2026-06-27-08`。

**過渡性**：wss化（案B）で plugin が WebSocket+TLS を内蔵すれば bridge は薄く/廃止（scratch-plan §将来）。ゆえに bridge に重いロジックを持たせず薄く保つ。

---

## モノリポ構成（mc-remote/ workspace）

dir/scope は **`mc-remote/`（kebab）＝npm scope `@mc-remote/*`＝ドメイン mc-remote.com に一致**（DECISIONS `2026-06-27-08`）。scratch-editor フォークの root workspaces に `mc-remote/*` を別枠追加。全て private。

```text
mc-remote/
├── protocol/   @mc-remote/protocol   leaf：型+定数（method名/PROTOCOL_VERSION/error reason/封筒）。依存なし
├── bridge/     @mc-remote/bridge     Node：wss⇄TCP 中継。deps: protocol            ← b1 実装
└── live/       @mc-remote/live       Node/TS：observer UI（ブランド WireScope）。deps: protocol  ← 配置予約のみ・実装 bN
```

- **vm 拡張は protocol を import せず inline 維持**（build-time bake・上記「型共有」）。
- **live（WireScope）= observer＝消費者**で protocol を所有しない（所有させると bridge が兄弟実装に依存する層逆転＝却下）。経路は live → bridge → plugin の wss。
- **live の wire は observer intent**で `2026-06-25-05`（hello role/intent を 21.0.0 に含めず後段）ゆえ **b1 実装は protocol と bridge のみ**。live は場所と名前の予約：空 dir は `mc-remote/*` glob が package.json 無しで警告するため **b1 では `live/` を作らず DECISIONS/AGENTS に予約記載のみ**、実装開始（bN）時に workspace 追加。
- **プロダクト/UI ブランド＝WireScope**（package 名は中立 `@mc-remote/live`、画面タイトルは WireScope 表示）。standalone 独立を決めたら `live/`→`wirescope/`・`@mc-remote/live`→`@mc-remote/wirescope` に rename（依存者ゼロ＝安価）。外部 npm 公開化トリガ＝bridge/live が別リポ化 or 非 fork TS クライアント出現時に `@mc-remote/protocol` を publish。

---

## Scratch b1 release gate（2026-07-01 確定搬送）

Scratch b1 は plugin / PythonAPI b1 と同じ build model を収容する同期リリースとして扱う（DECISIONS `2026-07-01-10`）。

- b1 では `build.setWorld` と `build.setOrigin` を入れる。
- b1 の GitHub tag 名は `scratch-editor-2100.0.0b1` とする。GitHub release は pre-release flag ON とし、Latest にしない（DECISIONS `2026-07-02-04`）。
- Scratch UI では `setOrigin` の y は編集可能にしない。ただし Y を完全に隠すのではなく、固定値 `0` として見せる。表記例: `[建築原点(X, Y, Z) を (x), 0, (z) にする]`。実装は y=0 を送る。
- b1 の確定条件は `setWorld` / `setOrigin` が収容されていること。
- X/Y/Z 編集版は標準導線に入れない。教材で検証してから b2 以降で再評価する。

これにより、Scratch / plugin / PythonAPI の b1 で機能集合を揃え、差分を UI と教材の表現に限定する。

### Scratch origin の教材原則

Scratch では `origin.y` を mode として扱わせない（DECISIONS `2026-07-02-03`）。

- `setOrigin` の主目的は、水平に広がる world の中で複数プレイヤーが同居し、同じコードを自分の領域へレンダリングできること。
- Y 軸の学習は `setBlock` の y 引数で明示する。`Y_SEA + y` 等の式をユーザーが見える形で書き、隠れた origin Y オフセットにはしない。
- プレイヤー位置・クロスヘアの絶対/相対座標表示を将来入れるため、Scratch 標準 UI では Y 座標まで origin でずらす状態を作らない。
- `setWorld` は既存の world/dimension mode で、オフセットでは代替できないため許す。overworld の建築を get/set で nether に複製する等の教材にも使える。
- X/Z origin も、教材上は同一作品内で頻繁に切り替える mode ではなく、テンプレートや接続・別セッションの初期文脈として扱う方向で検証する。

未決: Scratch の「セッション」を、別タブ、再接続、保存済み `.sb3`、localStorage token とどう結びつけるか。origin をどの時点で固定する UI にするかは、この保存/再接続仕様と一緒に決める。

---

## 2. 各部分の詳細

### 2.1 なぜ bridge 方式なのか(経緯と根拠)

当初は「新しい Scratch のネットワーク制約」を回避するため localhost 中継を構想していたが、制約の正体はブラウザの混在コンテンツ仕様だと判明した。

- HTTPS ページからの **平文 ws:// 外部接続はブロック**される。一方 loopback(localhost)への ws:// だけは例外的に許可されてきたため、先行実装(Scratch 公式の Scratch Link、Raspberry Pi の OneGPIO 等)は localhost リレーに逃げていた。
- しかしその **loopback 例外は年々狭まっている**。Chrome 142(2025-10)で Local Network Access が導入され、localhost への接続にも許可プロンプトが出るようになった。8歳児にこのプロンプトを正しく許可させるのは難しい。Safari/iPad では事実上不可。
- **wss://(TLS)の外部接続は混在コンテンツにならない**。正規ドメインの bridge へ wss で繋げば、loopback 例外にも LNA プロンプトにも一切触れず、全プラットフォームで動く。

結論として、localhost リレーは斜陽の道であり、bridge(サーバー側中継)が本命。

なお bridge 採用は同時に、**ブラウザ経路の操作対象をホスト型サンドボックス(`sb.mc-remote.com`)に移す**ことを意味する。localhost リレー時代の「手元のローカルのマイクラ」像をそのまま bridge 図に持ち込まないこと。**家庭/ローカルのマイクラは同一 LAN 内利用に限定**(インターネット越しの外部公開は二重ルーター/CGNAT で不能＝2026-06-28-01・§2.3 追補)。**共有は外向き接続でホスト型公開サーバーに集約**する(＝ルート1。「家庭マイクラを外部リレー経由でネット越し操作」＝ルート2は退けた経路)。

箱庭・教室・VPS・XServer GAMEs・Velocity 配下構成の正本は [40-サービス運用/server-topology-design](../40-サービス運用/server-topology-design_ja.md)。本書は Scratch 体験側の設計を持ち、サーバー配置の詳細は 40-サービス運用側を参照する。

### 2.2 ドメイン構成

| ドメイン | 役割 |
| --- | --- |
| `scratch.mc-remote.com` | Scratch Editor(安定版)。ユーザーから見て「Scratch」なのでこの名前に統一 |
| `scratch-dev.mc-remote.com` | Editor 開発版(dev) |
| `bridge.mc-remote.com` | wss を受ける中継サーバー(1つに固定) |
| `sb.mc-remote.com` | Sandbox(Minecraft / McRemote plugin)接続先。Python API もここ |

- Editor と Bridge は同一 VPS / ホームサーバーの Caddy に同居できる(ホスト名で振り分け)。
- FQDN は各所(bridge の Origin 許可リスト、拡張の接続先、Caddy 設定)にハードコードされるため、早期確定が重要。

### 2.3 ホスティングと TLS

- **Caddy** をリバースプロキシに採用。Let's Encrypt の証明書取得・更新・再読込を **HTTP-01 で全自動**。certbot も cron も不要。
- 条件は VPS / ホームサーバーの **80・443 がインターネットから到達可能**なこと。ホームサーバーはルーターでポート開放して対応(対応可能と確認済み)。
- 【2026-06-28 追補】上記「ポート開放で対応可能」は**単段ルーター環境での確認**。**二重ルーター/CGNAT（マンション・モバイル回線）ではポート開放が効かず到達不能**になる。これは家庭の inbound 公開（外から到達可能化）が大手でも未解決という一般問題＝Minecraft Java 26.2 は P2P を最終前に撤去・Bedrock も Strict NAT で失敗（外部事実 `F-mc-multiplayer-nat`）。よって**共有はホスト型公開サーバーへ outbound 集約を正とし、家庭/ローカルは同一 LAN 内利用に限定**する（DECISIONS `2026-06-28-01`）。ホームサーバーの inbound 公開は到達可能な単段環境に限った任意オプション扱い。
- **DNS-01 / Cloudflare 移管は先送り**でよい。ワイルドカード証明書は、プラグインで wss 化するとき証明書自己発行の段階で、80番を開けられないレンタルサーバーなどの場合に初めて必要になる。
- Scratch Editor は **完全な静的ファイル**なのでサーバー負荷は軽微。GitHub Pages も選択肢だが、ビルド成果物の巨大さと管理の一元化を考え、**VPS で Bridge と同居**を推奨。配信速度が課題化したら Editor だけ後で CDN へ切り出せる(静的物なので移動容易)。

### 2.4 接続ブロック(Scratch 拡張)

標準導線は、作品に保存されるブロック引数ではなく **Settings → Minecraft Remote → 接続先**で Sandbox を選ぶ形にする。Language / Theme / Color Mode と同じ PreferenceMenu の見せ方を習うが、内部状態は表示設定と混ぜず `mcremoteConnectionTarget` reducer / `localStorage` に保持する。接続先はブラウザごとの実行環境設定であり、`.sb3` に保存される作品状態ではない。

- `[マインクラフトに接続]` — 引数なし。GUI で選択中の Sandbox へ接続する。初心者・大多数の生徒はこれだけ使う。
- 接続先メニュー — Settings 内のブラウザ実行環境設定。固定プリセットから Sandbox を選び、選択値は `localStorage` 等に保存する。b2 のトップバー独立メニューはこの完成までの暫定面とする。
- `[マインクラフトサーバー( sb2.mc-remote.com )に接続]` 相当の引数付き導線 — デバッグ用 URL / 上級者 / 互換用。一般導線と教材には出さない。

設定へ収容しても接続状態は隠さない。McRemote のコマンドパレット内、信号機インジケーター直下に「設定上の次回接続先」と「実際に接続中の相手」を表示する。両者が違う場合は「再接続で反映」と文字でも示し、色だけに依存しない。

**bridge は常に1つ。** ユーザーが選べるのは Sandbox のみ。Editor は常に同じ bridge へ wss 接続し、WSS URL query に「繋ぎたい Sandbox の宛先」を載せる。既定形は `wss://bridge.mc-remote.com/?sandbox=sb-dev.mc-remote.com`。bridge はそれを allowlist で検証し、該当 Sandbox へ TCP を張る。`hello` には Sandbox を載せない。

```text
[Editor] --wss (?sandbox=sb2.mc-remote.com)--> [bridge] --TCP--> [指定された Sandbox:25575]
```

#### bridge は許可リストを持つ(確定)

bridge の設定に「繋いでよい Sandbox」の一覧を持ち、WSS query の指定がリストにあれば繋ぐ、なければ拒否する。

- 理由:許可リストがないと bridge が **任意ホストへ繋ぐ踏み台(SSRF / ポートスキャン中継)** になりうる。許可リスト方式なら未登録の宛先を弾ける。
- 新しい Sandbox を足すときは bridge 設定に1行追加するだけ。「運営が認めた Sandbox の中から選ぶ」形になり、安全性と自由度を両立。

#### 接続先メニューと学校運用

b2 の接続先メニューは、固定プリセットを選ぶ最小仕様に留める。任意接続先追加、接続先リストの import / export、教室・団体向けの配布、先生向け管理 UI、bridge URL の切替は b3 以降へ送る。

接続先メニューは、従前の「引数付き接続ブロックはデバッグ用 URL 起動時のみ表示し、一般には出さない」方針と矛盾しない。一般導線を GUI 設定へ移すことで、作品の `.sb3` と実行環境を分離したまま、学校導入で想定されるクラス・学年・授業単位の複数 Sandbox 運用を扱える。

権限は各 Sandbox の McRemote plugin / LuckPerms が担う。利用者が接続先を選べても、建築権限はサーバーごとの `mcr.online` / `mcr.offline` / `mcr.build.range` で制限される。Minecraft 世界への参加権限と McRemote 建築権限は別なので、見学参加は可能なまま、リモコン操作だけを制御できる。

接続先変更時は、既存 WebSocket を別 Sandbox へ暗黙転送しない。UI は切断または再接続が必要な状態として扱い、次回の接続ブロック実行時に新しい接続先を使う。

#### Bridge は透明な中継(正本は plugin 側)

- **正本は McRemote plugin 側**。`pair_code` / `session_token` / `player_token` の発行・保存(hash)・検証はすべて plugin が持つ。
- **Bridge は透明な中継**に徹し、認証情報の中身を解釈しない。担当は **WSS 接続の終端、Sandbox allowlist、rate limit、ログ、TCP 中継**のみ。
- **WSS session = route context / TCP connection = 一時 transport**。plugin 側 TCP が閉じても bridge は JSON-RPC error reason を読んで WSS 維持/切断を分岐しない。browser 側 WSS を維持し、次の WS message で同じ Sandbox route へ再 dial する実装を既定にする。
- 各クライアント(ブラウザの localStorage、Python/CLI の `~/.config`)が持つ token は「控え」であり、正本ではない。プロトコルの進化(コマンド追加・認証フロー変更)で Bridge を更新せずに済む。

### 2.5 認証仕様

#### 基本方針

```text
token   = 誰の接続かを証明する
LuckPerms = その人が何をできるかを決める
```

- クライアントが名乗るプレイヤー名は信用しない。token から `player_uuid` を復元し、権限判定は常に UUID に対して LuckPerms で行う。
- 管理者専用 token・先生専用 token・admin API key のような特権概念は作らない。すべての長期認証は `player_token` として扱い、管理者かどうかは毎回 LuckPerms で判定する。
- この分離により、token に権限を焼き込まずに済み、失効管理が単純になる。

#### token 種別

| 種別 | prefix | 有効期間 | 用途 | 保存先 |
| --- | --- | --- | --- | --- |
| `pair_code` | (6桁数字) | 約2分・1回限り | Minecraft 内での本人確認用コード(token ではない)。wire は素6桁、UI 表示は `NNN-NNN` | — |
| `session_token` | `mcrs_` | 約2時間 | Scratch、体験授業、共有PC、Pythonの明示一時利用 | クライアント形態ごと(後述) |
| `player_token` | `mcrp_` | 長期 | Python CLIでloginした先生PC、教材開発PC、自宅PC、常設端末 | `~/.config/mcremote/` 等 |

- token 本体は十分な乱数(例:32バイト)。サーバー側は **ハッシュのみ保存**(`store_hash_only`)。
- `player_token` は**デバイスごとに発行**し、`last_used_at`を記録。紛失時に1台だけ無効化できる。永続hash store / list / revokeが完成するまで公開導線では発行しない。現時点ではbearer tokenなのでファイルcopyでも動作し得るが、非推奨でありPoPを実装済みとは扱わない。
- Scratchの標準導線はsession tokenだけを要求・発行・保存する。player tokenやPython credentialをScratchへcopy / exportしない。

#### ペアリングの流れ(短期)

1. クライアントが bridge / plugin へ `pair_begin` を送る
2. plugin が6桁 `pair_code` を発行
3. クライアント側にコードを表示
4. プレイヤーが Minecraft 内で `/mcremote pair <code>` を実行
5. plugin がコマンド実行者の UUID を取得し、pending 接続を UUID に紐づける
6. plugin が `session_token` を発行
7. クライアントは token を保存し、以後は再ペアリング不要で再接続

#### Scratch でのペアリング体験(具体フロー)

Bridge は常時稼働しているので「Bridge 起動」は体験に含めない。ユーザーから見た流れは以下。

1. **Editor を開く**:ブラウザで `scratch.mc-remote.com` を開く。
2. **セッション確認(自動)**:Editor が `localStorage` の `session_token` を確認する。
   - 有効な token があれば、`[マインクラフトに接続]` ブロック実行時にそのまま接続でき、ペアリング不要。
   - 無い / 期限切れなら、次のペアリングへ進む。
3. **接続先を選ぶ**:必要なら GUI の接続先メニューで Sandbox を選ぶ。選択はブラウザ実行環境の設定であり、`.sb3` には保存しない。
4. **接続ブロックを実行**:`[マインクラフトに接続]` を置いて実行する。デバッグ用 URL / 上級者導線では引数付き接続ブロックを使える場合があるが、標準導線では使わない。
5. **6桁コードの表示**:Editor が `pair_begin` を送り、画面に6桁の `pair_code` を `NNN-NNN` 形式で表示する(例:ステージ上の変数 / 専用パネル)。「Minecraft の中で `/mcremote pair 827-419` と打ってね」と案内し、コピー対象はコマンド全体を既定にする。
6. **Minecraft 内で本人確認**:プレイヤーが Minecraft 内で `/mcremote pair <code>` を実行。plugin がコマンド実行者の UUID を取得し、pending 接続に紐づける。
7. **接続成立**:plugin が `session_token` を発行 → Editor が接続先別に `localStorage` へ保存 → `[ペアリングできたとき]` ハットブロックが発火し、プログラムが動き出す。
8. **以後**:session_token の有効期間内(約2時間)は、同じ接続先への再接続ではペアリング不要。期限切れ・拒否時は現在接続先の token だけを破棄して 5 に戻る。

ブロック構成(目安):

- `[マインクラフトに接続]` — 接続開始(ハンドシェイク hello)。デバッグ用 URL / 上級者導線では引数付き接続ブロックを使える場合がある。
- 接続先メニュー — 現在の Sandbox を選ぶ GUI 設定。ブロック引数ではなく、作品には保存しない。
- `(ペアコード)` — 6桁を表示するレポーターブロック
- `[ペアリングできたとき]` — 完了イベントのハットブロック

ポイント:秘密(token)はブラウザの `localStorage` に保持し、ブロックには露出させない。子供が見るのは6桁のペアコードのみ。8〜80歳に過不足ないフロー。

#### token の保存先(クライアント形態ごとに異なる / サーバー検証は共通)

- **Scratch(ブラウザ)**: `localStorage`(オリジン `scratch.mc-remote.com` で隔離)。session_token は低価値・2時間失効なので十分。token は接続先別に保存し、`sb.mc-remote.com` の token を `sb-dev.mc-remote.com` や校内 Sandbox へ送らない。認証系 reason（`auth_required` / `token_expired` / `token_revoked` / `token_not_found` / `token_invalid`）では現在接続先の token だけを破棄し、`permission_denied` では token を温存する。
- **Python / CLI**: `~/.config/mcremote/`(`$HOME` 起点。Linux は `$XDG_CONFIG_HOME` 優先、macOS も `~/.config` で統一可、Windows は `%APPDATA%`)。owner-only permissionを使う。
- 同一プレイヤーの複数デバイスを想定。credentials はデバイス名キーの配列で追記する。
- credentialは接続先profile / targetへ紐づける。stable / beta / alphaや別Sandboxのtokenを黙って流用しない。Scratchのtoken、接続先、将来の秘密鍵を`.sb3`へ保存しない。

#### player_token 発行フロー(CLI)

```text
mcremote login --channel beta
mcremote login --host example.com --port 25575
```

1. CLI が `pair_begin` を送る → 2. plugin が6桁 `pair_code` を返す → 3. CLI が表示 →
4. Minecraft 内で `/mcremote pair <code>` → 5. plugin が UUID を確認 →
6. CLI 用に `player_token` 発行 → 7. CLI がユーザーホーム配下に保存 →
8. plugin が token_hash とメタ情報を `player_tokens.yml` に保存

`--channel stable|beta|alpha`は公式接続先profileを選ぶ引数でありpackage版の指定ではない。裸の`mcremote login beta`は採らない。CLIは`login / status / logout / devices / revoke`を扱い、`Minecraft.create()`は非対話とする。credentialが無い・期限切れ・revoke済みの場合は自動pairを始めず、実行すべき`mcremote login ...`を含む例外を返す。共有PC等の短期利用には`--session`を明示する。

#### 権限判定(LuckPerms)

権限名は既存 `config.yml` の設定名に従う。

能力権限:

```text
mcr.online      オンライン状態での通常リモコン操作
mcr.offline     オフライン状態でもリモコン可能にする特殊権限(初期 Scratch 対応では主対象外)
```

meta key(値を持つキー。能力権限とは別物):

```text
mcr.build.range   建築範囲グループを表す meta key
```

- 認可は token 種別ではなく常に UUID → LuckPerms で判定する。
- オフライン実行の可否は token 種別ではなく `mcr.offline` 権限で決まる(生徒はオンライン必須、先生はオフライン可)。詳細は管理者向け特殊機能として扱い、本計画では深入りしない。

#### エラーコード

認証系と認可系を分離する(クライアントの自動再ペアリング判定が単純になる)。

- 認証系:`TOKEN_EXPIRED` / `TOKEN_REVOKED` / `TOKEN_NOT_FOUND` / `TOKEN_INVALID` → token を捨てて再ペアリング
- 認可系:`PERMISSION_DENIED` → token はそのまま、操作だけ拒否

### 2.6 脅威モデルと割り切り

箱庭サーバーは一般公開・ホワイトリストなし・profile別backup・必要時world resetが前提で、**worldは壊れても復元・再生成できる実行結果**として扱う。主要な保護対象はhost OS、秘密、他service、家庭LAN、availabilityである。これに基づき:

- **ペアリング逆方向攻撃**(攻撃者の pair_code を被害者に打たせ、攻撃者接続を被害者 UUID に紐づける)は **対策しない**と明示的に決定。守るべき資産がない(建築は消えてよい)ため、UI 確認を挟んでも騙される子は騙され、体験を複雑にするだけ。
- **TLSで守られるのはブラウザ→bridge区間のみ**。bridge→SandboxとPython direct TCPは平文でtokenとcommandが流れる。この残余riskを明示した上で、箱庭betaをTLS完成まで一律停止しない。通常のoff-path利用者が既存TCP connectionへ容易にcommandを注入できるわけではなく、能動的on-path攻撃を守るには接続時PoPだけでも足りない。
- **PoPは現release gateに含めない**。token文字列だけを別端末の新規接続で使う攻撃には効くが、暗号化、認証後改ざん、DDoS、端末/同一Origin JavaScript侵害、plugin脆弱性、world破壊を解決しない。Web Crypto / IndexedDBの非export鍵、challenge / proof、Python鍵保管は将来hardeningとしてparkし、wire値を先取りしない。
- **DoS / overloadを優先する**。認証前connection/frame/timeout/pairing rateと、認証後session/inflight/queue/tick workload/backpressureを分け、正規の大量建築・TNTもbudgetとtick分割でboundedにする。Scratchはthrottle / backpressure / cancelを状態UIとWireScopeへ表示し、単なる「接続失敗」に畳まない。

#### Bedrock / Geyser の UUID(要実機確認)

- Floodgate は XUID を `00000000-0000-0000-xxxx-xxxxxxxxxxxx` 形式の決定論的 UUID に変換するため、同じ Bedrock アカウントは常に同じ UUID。`/mcremote pair` 方式は Bedrock でもそのまま機能する見込み。
- 注意:`online-mode=true` 前提(オフラインモードだと UUID 不整合)。LuckPerms は `allow-invalid-usernames` 等の Floodgate 向け設定が要る場合あり。**pair 実装後に Bedrock 実機で1回通すこと**(未検証ゾーン)。

### 2.7 iPad / モバイルでの体験

#### iPad での Scratch 体験

- iOS/iPadOS では、自作アプリ内ローカルサーバーも WKWebView 経由のローカル接続も Local Network Privacy で塞がれる方向。localhost リレー方式は iPad で事実上不可。簡易ブラウザ自作も投資に見合わない(Scratch 公式すら Safari 拡張という飛び道具で解いた)。
- **しかし bridge 方式(wss で正規ドメイン `bridge.mc-remote.com` へ)なら、この制約に一切触れない。** iPad の Safari で `scratch.mc-remote.com` を開くだけで、PC とまったく同じ体験ができる。追加アプリのインストールも、ローカルサーバーの起動も不要。
- ペアリング体験も PC と同一(2.5 のフロー)。iPad で Scratch を開き、別途 Minecraft(統合版など)で `/mcremote pair <code>` を打てば繋がる。**iPad は bridge 方式を採る最大の受益者**であり、構成選択によって「対応不可」から「無改造で対応」へ変わった。
- 注意:保存層のうち IndexedDB 自動保存は、iPad Safari がストレージを自動退去させることがある(未使用時)。iPad ユーザーには特に「大事な作品は .sb3 ダウンロードかクラウド保存を」と促す。

#### iPad での Pythonista 体験(Python 入口)

- iPad で Python を書く層には **Pythonista**(iOS 上の Python 環境)を想定。`minecraft_remote_api` を使い、TCP で Sandbox(`sb.mc-remote.com:25575`)へ直接接続する。
- Pythonista は **WebView を介さずアプリ自身が TCP クライアント**になるため、Local Network 制約の影響を受けにくい(ブラウザ経由ではない)。bridge は不要で、Python クライアントと同じ経路。
- 認証は **player_token** が適する(継続利用・常設端末向け)。token は Pythonista のファイルシステム配下(`~/Documents` 相当)に保存。`mcr.offline` を持たない通常ユーザーはオンライン在席が必要な点は PC と同じ。
- 位置づけ:**iPad の Scratch 入口は bridge 経由(ブラウザ)、Python 入口は Pythonista から直 TCP**、と経路が分かれる。どちらも追加のローカルサーバーは要らない。

### 2.8 保存層(三層モデル)

改造版 Scratch はローカル起動時に既存セーブ機構が隠れる。**既存機構は触らず、すべて新規追加**で実装する(追従コスト削減のため)。

| 層 | 位置づけ | 内容 |
| --- | --- | --- |
| IndexedDB 自動保存 | 揮発前提のバックアップ | 変更時デバウンス保存。開き直すと復元。"保存"ではなく"オートセーブ"と明示。共用 PC 向けに複数プロジェクトをキーで保持 |
| .sb3 ダウンロード/アップロード | ポータブルな**正本** | 標準機能。クラウドが落ちても標準 Scratch / TurboWarp で開ける。ロックイン回避の思想的な要 |
| 匿名クラウド保存 | 共有・提出・リミックス | URL 限定公開・**上書きせず毎回新 ID 保存**・公開前提 |

ブラウザ内ストレージは用途で使い分け、**統一しない**:

- `localStorage` = **session_token**(認証の控え)。小さく同期的に読めればよい。
- `IndexedDB` = **作品の自動保存**(.sb3 シリアライズ結果)。大きいバイナリ向き。
- 役割が違う(認証情報 vs 作品データ)ため、無理に1つのストレージへ統合しない。

#### 匿名クラウド保存 API

URL 設計(Editor と同一オリジンに同居、CORS 不要):

```text
scratch.mc-remote.com
  /                  Editor
  /project/<id>      Project view/load(人間向け閲覧 URL)
  /api/projects      Save/load API(機械向け)
```

- **保存**: `POST /api/projects`(body は .sb3 バイナリ)→ `id` と `delete_token` を返す。上書きエンドポイントは作らない。
- **読込**: `GET /api/projects/<id>` → .sb3 を返す。`/project/<id>` はこれを自動ロードする薄いラッパー。
- **削除**: `DELETE /api/projects/<id>` + `delete_token`。不一致は 403。

設計上の要点と理由:

- **ID は推測困難なランダム**(URL-safe 20文字以上)。連番は総当たり閲覧で「URL 限定公開」が崩壊するため厳禁。`parent_id` を任意で持てばリミックス系譜を追える。
- **毎回新 ID(イミュータブル)**はリミックス文化と相性が良い。提出はスナップショットとして凍結、リミックスは自然に枝分かれ(追記只進モデル)。
- **delete_token** はサーバーにハッシュのみ保存。匿名性と削除可能性を両立(pastebin の delete key 方式)。
- **メタデータ**:作成日時・最終アクセス日時・サイズ・parent_id・delete_token ハッシュ。投稿者特定情報は持たない。

容量・レート制限(入れると確定。具体値は叩き台):

- 1ファイル上限 5〜10MB(超過は 413、画像・音を減らす案内)
- IP あたり保存レート 例:1分5回・1日100回(匿名・無認証はスパムの的)
- 自動失効:最終アクセスから90日アクセスなしで削除(GET で最終アクセス更新 → 使われる作品は生存)。学期またぎ需要があれば 180日等に調整
- 総量の番兵:ストレージ全体の上限監視・アラート

子供向けの配慮:

- 保存時に「URL を知る人なら誰でも見られる/個人情報を書かない」を明示
- 通報・削除依頼の窓口、運営による特定 ID の非公開化・削除手段

実装:bridge と同じホスト上の小さな HTTP サービス1本。保存先はファイルシステム(`<id>.sb3`)+ メタを SQLite が最も単純。Editor(静的)/ Bridge(wss)/ 保存 API(http)が役割分離され、独立に開発・テストできる。

### 2.9 Scratch Editor の追従戦略

> 移行注記（2026-07-18）: 本節の機構（branch 表・定例フロー・頻度）は [scratch-upstream-design](scratch-upstream-design_ja.md)（起案・DECISIONS `2026-07-18-02`）へ委譲。追従と upstream 貢献は二トラックへ分離し、branch 表の `upstream/main` は monorepo 移行後の実態では公式既定 branch `develop`。本節の本質原則（衝突する変更量の最小化・同じ場所を触らない設計・3カテゴリ管理）は不変。

放置すると追従困難になる原因は**経過時間ではなく衝突する変更量**。よって「upstream と同じ場所を触らない設計」が本質、頻度はその次。

改造を3カテゴリに分けて管理:

1. **純粋な追加(衝突ゼロ)**:McRemote 拡張本体、保存層モジュール、独自コンポーネント。新規ファイルなので永遠に衝突しない。改造の大半をここに寄せる。
2. **登録のための最小パッチ(低リスク)**:拡張をライブラリに登録する数行、保存メニュー差し込み。`// === MC-REMOTE PATCH START ===` 等のマーカーコメントで囲み、コンフリクト解決を機械的にする。
3. **upstream コードの改変(高リスク・最小化)**:既存挙動の書き換え。ラップ/フック/新規追加で迂回し、できる限り避ける。

リポジトリ:`github.com/Naohiro2g/scratch-editor`

| ブランチ | 役割 |
| --- | --- |
| `upstream/main` | Scratch 公式 scratch-editor |
| `mc-remote/main` | McRemote 版の開発主軸 |
| `mc-remote/stable` | 授業・公開用の安定版 → `scratch.mc-remote.com` |
| `mc-remote/dev` | 新機能・追従テスト用 → `scratch-dev.mc-remote.com` |

定例フロー(マージ推奨。公開リポでのリベースは破壊的):

1. `upstream/main` を定期更新
2. `mc-remote/dev` に `upstream/main` をマージ → コンフリクト解決(マーカーのおかげで機械的)
3. `scratch-dev.mc-remote.com` で回帰確認(拡張・保存層・基本機能)
4. 問題なければ `mc-remote/main` 経由で `mc-remote/stable` へ昇格 → `scratch.mc-remote.com` 更新

頻度:**月1回の定例 + 重要変更時の臨時**。最初の1回はフル追従(溜まり分が重い)、以降は差分を小さく保つ。コードの衝突よりビルド設定・依存・ディレクトリ構成の変更(例:モノレポ移行)が追従を苦しめるため、小さく定期的にやることで構造変更も「小さな揺れ」の連続として吸収する。

サーバー構成の注意:

- bridge の Origin 許可リストに **stable と dev の両方**を入れる(`https://scratch.mc-remote.com` と `https://scratch-dev.mc-remote.com`)。さもないと dev Editor からの wss が弾かれる。
- **Bridge は1つ共用、Editor は stable/dev を分け、Sandbox は allowlist 内の profile として選ぶ**。通常のEditor検証は同じ箱庭でもよいが、plugin / worldを含む結合試験は `sb-dev` を使う。Bridge自体を本番・開発で二重化しない。（改訂 2026-07-19: Bridge は実装共通・instance は channel 別へ＝`2026-07-19-02`、server-topology-design §5 配置フェーズ）

---

### 2.10 Color Mode と状態表現

Scratch本体の `Color Mode: original / high-contrast` に追従し、McRemote独自UIにも同じmodeを投影する。拡張アイコン、接続インジケーター、ペアコード、通知、WireScopeを対象に visual regression を持つ。

- 接続・警告・無効状態は、色に加えて形、アイコン、短い文字を必ず併用する。
- 黄色系の注意表現には黒枠を付け、high-contrastではScratch側tokenへ切り替える。
- キーボード操作、visible focus、スクリーンリーダー名を独自UIのgateに含める。

### 2.11 お知らせオーバーレイと展示版

Scratchワークスペースは縦1pxも恒常的に減らさない。閉じた状態では Scratchロゴ左上に小さな黒枠付き `▶` だけを重ね、独立した一行を残さない。見た目の三角は小さくても、透明paddingで十分なhit targetを確保する。

開くと `▲`、黄色系背景、見出し、本文、任意リンクを持つ overlay を表示し、ワークスペースをreflowしない。Enter / Spaceで開閉、Escapeで閉じ、focusを適切に戻す。**reload時は必ず開く**。閉じた状態を `localStorage` / cookie へ保存しないため、新しいお知らせと展示版の注意を見逃さない。

runtime config は `deploymentProfile`、capabilities、notices を持つ。GitHub Pages は `showcase` profile とし、次を二重に固定する。

1. build時に接続コードを無効化または到達不能にする。
2. runtime capability でも `minecraftConnection: false` を設定する。

token読出しやWebSocket生成より前の共通guardで拒否する。ブロックと実装形態は見せ、実行時には「このページはサーバー接続機能を無効化した展示版」と説明する。Pages更新は当面、release tagを選ぶ手動 `workflow_dispatch` とする。

### 2.12 WireScope の役割と配置

Scratch内のWireScopeは「今どうなっているか」を示す薄い観測面にする。右上は選択中スプライト表示と衝突するため避ける。

| 面 | 役割 |
| --- | --- |
| パレット内 | 接続状態、設定先、実接続先、直近エラーを常時コンパクト表示 |
| 折り畳みパネル | セッション概要。block workspace下部のdrawer / overlayとし、Backpackとは相互排他で開く |
| payload詳細 | frame / payloadを開いた時だけ既存の広い幅を使う。payloadがなければ狭くする |
| WireScope app | 全frame、検索、比較、長時間観測を引き取る standalone app |

パネルに `WireScopeで開く ↗` を置き、runtime config のURLを `noopener,noreferrer` 付き別タブで開ける。初期版で渡すのはSandbox route等の非秘密情報だけとし、tokenをURLへ入れない。認証済みhandoffが必要になったら、短命・一回限りのlaunch ticketと厳格な `postMessage` origin検査を別設計する。

スプライトごとの「コード／コスチューム／音／マイクラリモコン」第4タブは、per-sprite streamが実在して価値が出るまでparkする。現在はScratch内の薄い状態面と外部WireScope appの分担を正とする。

### 2.13 ブラウザ保存作品・クラウド保存

Scratch本家の「私の作品」に相当する入口はフォルダアイコンを維持し、表示名を **「ブラウザ保存作品」** とする。IndexedDBの複数オートセーブと、このブラウザから作った匿名クラウドsnapshotの索引を一覧化する。「アカウントの作品」や端末間同期とは呼ばない。

クラウドは保存ごとに新IDを作るが、ローカルの `projectKey` / lineageでまとめ、履歴が一覧を埋め尽くさないよう最新snapshotを主表示にする。匿名保存時の操作は次とする。

```text
[クラウドに保存]
  → [リンクをコピー] [プロジェクトページを見る] [.sb3を保存]
```

`[共有する]` は、公開コミュニティ、アカウント、moderationを持たない段階では表示しない。`/project/<id>` は作品をロードする薄いページとし、Editorで開く、リミックス、`.sb3`取得を提供する。

### 2.14 Backpack・チュートリアル・デバッグ

Backpackは同一originのブラウザタブをまたいで使える小さな素材棚とする。IndexedDBを正本、BroadcastChannelを更新通知に使う。最初からフォルダ階層や大量タグを作らず、名前、種類filter、検索、最近使った8〜12件、pin、削除で「放り込みすぎて分からない」を抑える。

Scratch既存のTutorial deck / category / tag / `?tutorial=` / starter projectを再利用して、McRemoteの最初の接続、ペアリング、最初の1ブロック、座標、保存を案内する。役割は分ける。

- チュートリアル: 手を動かす順序。
- デバッグ: エラー概念と、直近エラーから該当説明へのdeep link。
- Scratch内WireScope: 現在状態。
- WireScope app: frame / payloadの詳細調査。

## 3. プラン進行(時間軸)

旧 Phase 0〜2（fork build、McRemote拡張、bridge/pair疎通）は `2100.0.0b2` までに実質完了した。旧 Phase 3「ホームサーバーへのCI deploy」と Phase 4「後でVPS移行」は、VPSを固定本番面にし release / deploy を分離する現在方針で置き換える。

### 現在: b2 close / R2完了、R3-A進行中

- plugin / Python / Scratch の認証・bridge・接続先・WireScope v0 を同期release済み。
- b2 tagからの配布とmainline cleanupを完了。
- `.sb3` 旧互換はb3送り。R3の三層保存完了とは数えない。

R3-A完了済み（2026-07-20）:

- 6GB VPSへCaddy / stable Editor / beta Editor / Bridge stable・beta instanceをprofile展開し、Phase 1のbeta Minecraftへb2をexact lockでdeployした。旧protocol stableは正規名`sb.mc-remote.com`のままGAMEs無料へ一時退避した（`2026-07-20-07`）。
- official VPSのreference deploymentで、不変artifact / exact lockからdeploy→smoke→rollback→stable smoke→同一構成redeployを一周し、構成hash一致とbeta human pairingまでPASSした（[rollback rehearsal](../14-evidence/records/2026-07-20-official-vps-beta-rollback-rehearsal_ja.md)）。
- stable / beta Editorの接続先候補をruntime configから供給し、配備既定を`sb.mc-remote.com` / `sb-beta.mc-remote.com`へ固定した。旧候補が`localStorage`に残る場合は配備既定へ戻し、公開configにはloopback等のlocal候補を含めない。
- Scratch CIのcaller / reusable workflow権限不整合を最小権限で修復し、修復mergeと後続`develop`でBuild / Test Resultsのsuccessを再現した。required checksの強制は次回Scratch release gateに残す。

### 次: R3-A残り

- Ubuntu home host 2のalphaはtag前source commitを動かすLAN/VPN限定環境とし、`bridge-alpha`（home側instance）で完結させる（公開TLS面にalpha入口を作らない＝server-topology-design §5）。
- GitHub Pagesへ接続無効のshowcase profileを手動tag指定で配布する。
- Settings接続先UI（runtime configによる候補供給は完了）、パレット状態表示、Color Mode、お知らせoverlayを完成する。

### R3-B 保存・学習・beta体験

- 旧 `.sb3` load/save互換を直し、三層保存を完成する。
- 「ブラウザ保存作品」、匿名クラウド、`/project/<id>` を実装する。
- McRemote Tutorial / Debug導線、最初の1ブロックまでの教材を揃える。
- iPad/Safariを含む数分オンボーディングと、作例数本をR3 gateで確認する。

### R3-C 運用パッケージ拡張

- ServerBackup紹介・外部transfer・restore手順を同じ運用パッケージへ追加する。world restoreとcredential storeを分離する。
- 認証前後のavailability guard、Cockpit / Paper同梱spark / McRemote metric、正規bulk build / TNTのload testを公開beta gateへ追加する。
- Nextcloud/WebDAV adapterはMcRemote外の独立pluginとして後続させる。
- WireScope appの起動導線と、Backpackの小さなMVPを追加する。初回betaをブロックするかは実装規模で切る。

### R3後 / 並行

- **transport選択**: 同一LAN → port forward/hairpin NAT → VPN/overlay → generic reverse tunnel → McRemote-aware reverse Gatewayの順に必要性を評価する。Scratchから利用者所有LAN Minecraftへ到達する需要が一定以上になった時だけreverse Gatewayを取り出す。
- **plugin native WSS/TLS**: Bridgeの運用負荷、latency、配備制約に実害が出た時の選択肢。direct TCPをsocket教材として残し、Bridge / TLS / reverseの全組合せを需要前に作らない。
- 備え:接続経路・Sandbox 指定は WSS 接続メタ（`?sandbox=...`）へ寄せ、`hello` は protocol/auth/build に絞る。Bridge を外す日は拡張の接続先 URL を Sandbox 直結へ変えるだけで済む。
- per-sprite streamが実在した時点で、第4タブ「マイクラリモコン」を再評価する。

---

## 4. 次の作業候補

- **ワイヤ形式仕様**（旧称「プロトコル v1 仕様書」）は [10-protocol/wire-format-design](../10-protocol/wire-format-design_ja.md) に着地済み（DECISIONS `2026-06-26-01`）。エンベロープは **JSON-RPC 2.0**（要求 `{jsonrpc,id?,method,params}`／応答 `{jsonrpc,id,result|error}`）。bridge 経由でも将来の直結でも同一プロトコルで動く。
- **`setPlayer` は廃止し `hello` に吸収**。pair で UUID が確定するため「名乗り」コマンドは不要になり、接続確立(hello)が認証・protocol/build 交渉を担う。Sandbox 指定は bridge の WSS 接続メタが担う。これによりなりすまし問題が消える。
- **MVP コマンド**(helloは接続ハンドシェイクで、以下の実行コマンドとは層が別。`method` は TCP ドット名直結):
  - `hello` — 接続ハンドシェイク(auth + protocol/build)。1接続に1回。params は object（hello のみ）。Sandbox routing は bridge の WSS query で指定する。
  - `chat.post` / `world.setBlock` / `world.setBlocks` / `world.getBlock` — 実行コマンド。params は位置配列。
- **将来追加**:`getPlayerPosition` と、それを起点にする player-position-based commands。座標系・取得タイミング・誰の位置かの設計を詰めてから入れるため MVP 外。

### 4.1 履歴スナップショット: クライアント実装状況（2026-06-26、b1前）

以下はb1前のギャップを保存した履歴であり、現在の次作業一覧ではない。b2で解消済みかどうかは release gate / DECISIONSを正とする。

- `scratch3_mcremote/index.js` は **DRAFT エンベロープを実装済み**（DECISIONS `2026-06-26-01`：P-1 確定・hello P-2 起案・残り未確定は wire-format-design §6/§7）。確定で JSON-RPC 2.0 へ寄せたため、DRAFT（独自最小形 `{id?,cmd,args}`）からの追従改修が要る（`cmd`→`method`・`args`→`params`・`jsonrpc:"2.0"` 付与・error を `{code,message,data}` 形へ）。**bridge/plugin の TCP 原子 flip（`2026-06-26-02` live-state）に同期＝中間相互運用形が無いので scratch 単独先行は不可**（hub NOTES `2026-06-26 横断` TCP payload 原子ステップ）。
- **TODO（カタログ）**：`BLOCK` を自由入力 → **生成カタログ由来プルダウン**へ（起案 `2026-06-26-03`／wire-format-design §7.2）。**IndexedDB キャッシュ**（オリジン×`catalogHash` キー）＋同梱既定版フォールバック。接続後にサーバ版で差し替え。block id は文字列名（無印=`minecraft:`・§7.1）。
- **既知ギャップ**：WS close 時に `_pending` を reject しておらず、**`world.getBlock` が接続断でハングし得る**。wire-format-design §3.4/§9。v1 で timeout / close-reject を規定するか実装 TODO 止まりかは要決定。【2026-07-04 **b2 スコープ入りで決着**＝WS close 時の `_pending` reject 修正は b2 準核・接続状態 UI の実装と同じ工事で回収（`2026-07-04-03`・versioning §10.11.1 項10）】
- `hello` は現状 `[sandbox?]` の**位置引数のみ**。P-2 ratify 後に Sandbox 指定を WSS query へ移し、`hello` は object 化＋auth/build/version 対応へ更新（`_hello()` 直上に TODO 有り）。**ratify は §8 広告（mc_version/supported_mc_versions）整合待ちで保留**（wire-format-design §6）。

---

## 5. 次セッションの開口

第一候補は §3 の **R3-A残り**。Ubuntu home host 2へLAN/VPN限定のalpha profileを構築し、その後、GitHub Pages showcaseとScratch側のSettings接続先・状態面・Color Mode・notice capabilityを一つのUIスライスとして進める。official VPSのprofile展開、deploy / rollback / redeploy、stable / beta runtime config、Scratch CI修復は完了側から再開しない。

Velocity / Gateway、Bedrock UUID実機確認、plugin直wss、per-sprite tabはR3-Aの開口へ混ぜず、各正本のparkを維持する。
