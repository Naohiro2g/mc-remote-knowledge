# 設計記録: McRemote ワイヤ形式（JSON-RPC 2.0 エンベロープ）

> マイクラリモコン（Code2CreateClub / mc-remote.com）設計記録
> 関連: `Naohiro2g/McRemote`（プラグイン）, `Naohiro2g/minecraft-remote-api`（API）, `Naohiro2g/scratch-editor`（Scratch クライアント）
> 出典: scratch-editor 作業セッション 2026-06-26（`scratch3_mcremote/index.js` の DRAFT 実装でピン留め）
> 結節点: [versioning-design] §3（メジャー増分）/§8（hello ネゴ）/§10.11（protocol 21.0.0）と直結。本文書は**ワイヤ符号化の SSOT**で、版判定規則の正は versioning-design §8。

---

## 1. 位置づけ（protocol semver との関係・用語の整理）

本文書は**プラグイン ↔ 各クライアントの実際のワイヤ符号化**（フレーミング・エンベロープ・コマンド表・エラー形）を定める。これは [versioning-design] が扱う **protocol semver（20.0.0 / 21.0.0…）とは別レイヤ**。

- **エンベロープ形式版** ＝ `jsonrpc: "2.0"`（JSON-RPC 2.0 を採用、§3）。各メッセージに自己記述で載る。
- **protocol 版** ＝ semver（例 **`21.0.0`**）。互換判定は versioning-design §8（メジャー一致必須・`plugin.minor >= client.minor`・パッチ不問）。hello で交渉する。**package 版 `2100.0.0b1` とは別レイヤ**＝`b1` は配布チャンネル表記で **wire 非搭載**、hello の `protocol` フィールドには clean な protocol semver `21.0.0` を載せる（DECISIONS `2026-06-27-01`）。package は protocol から fold 規則（versioning-design `2026-06-19-04`）で派生＝独立ではない。

> **「protocol v1」という旧称について**：scratch-plan §4/§5 が「プロトコル v1 仕様書」と呼んでいたのは本文書のワイヤ仕様のこと。protocol semver の `1.x` とは無関係で混同しやすいので、本リポでは「**ワイヤ形式**」と呼び、semver は versioning-design の番号で呼ぶ。このワイヤ符号化が初めて載る protocol semver は **21.0.0**。`2100.0.0b1` はそれを載せる配布物側の prerelease 表記で、protocol 自体の beta ではない（versioning-design §10.11）。

---

## 2. トランスポートとフレーミング

トランスポートは**経路で2系統**ある。ブラウザ（Scratch）は混在コンテンツ制約から wss が必須（DECISIONS `2026-06-11-01`、外部事実 `F-loopback`）、Python は bridge を介さず直 TCP（`Minecraft.create()` が独立 socket）。bridge が wss ⇔ TCP を透過変換するため、プラグインから見れば bridge 経由の Scratch も直 TCP の Python も同等。

- **経路別フレーミング**（DECISIONS `2026-06-26-02`）：
  - **wss 経路**（ブラウザ/Scratch、bridge 経由）＝**1 WS メッセージ ＝ 1 JSON**。WS がメッセージ境界を持つため改行区切りは不要で、1 メッセージに複数 JSON を連結しない。
  - **直 TCP 経路**（Python クライアント／bridge→プラグインのホップ）＝**改行区切り（1行=1 JSON・`\n` 終端）**。TCP はバイト列で境界を持たないため枠が必須。**改行区切りは検証済み（2026-06-26、現 TCP read ループ）で、mcpi テキスト→JSON-RPC の payload 差し替えを跨いで不変**。JSON 化後は **compact 直列化を強制**し JSON 内部に生改行を出さない。bridge は WS 1 メッセージを 1 行に詰めて TCP へ流す。
- **bridge routing**（DECISIONS `2026-07-06-05`）：wss 経路の接続先 Sandbox は JSON-RPC payload ではなく WSS 接続メタで指定する。既定形は `wss://bridge.mc-remote.com/?sandbox=sb-dev.mc-remote.com`。bridge は `sandbox` を allowlist で検証し、該当 Sandbox へ TCP を張る。**WSS session は route context の寿命、bridge→plugin の TCP connection は一時 transport** とする。plugin 側 TCP close は browser 側 WSS close を必ずしも意味しない。bridge は JSON-RPC error reason を解釈して WSS 維持/切断を分岐せず、次の WS message が来たら同じ route context で再 dial できる。`auth_required` 等で plugin 側 TCP が閉じても、続く `auth.*` と再 `hello` を同じ Sandbox へ流す。直 TCP 経路では接続先 host/port 自体が route であり、wire payload には載せない。
- **非 JSON のメッセージ／行は破棄**。**未知の `id` を持つ応答も破棄**（id 相関で待ち先が無いもの）。両経路で共通。

> 検証済み（2026-06-26、両側実装）：直 TCP の境界は改行区切りで plugin/Python が一致＝Python `minecraft-remote-api`（branch `protocol-21.0.0-b1`、`mc_remote/connection.py` は送信時 `\n` 付与・受信 `readline().rstrip("\n")`）／plugin `McRemote`（`RemoteSession.java` の `BufferedReader.readLine()`）。既存の行指向プロトコルと地続き。
> **live-state（2026-06-26）**：現 TCP payload は旧 mcpi テキスト（`world.getBlock(x,y,z)`・カンマ区切り応答）で、JSON-RPC エンベロープ（§3・`2026-06-26-01`）は **TCP 経路に未着地**＝b1 残作業（フレーミング不変・payload のみ差し替え）。`connection.py`/`RemoteSession.java` を**同時に flip する原子操作**＝hello が新規で中間相互運用形が無いため、片側だけ差し替えると改行枠は生きてもパースが割れる。回帰ベースライン（差し替え前 mcpi 経路）を取ってから flip し、hello 疎通（Layer 1）を差し替え対称性の最初の証明とする（捕捉: NOTES 2026-06-26 横断）。

---

## 3. エンベロープ（JSON-RPC 2.0）

JSON-RPC 2.0 を採用する（採用判断と却下案は §8）。

### 3.1 要求（クライアント → サーバ）

```json
{ "jsonrpc": "2.0", "id": 1, "method": "world.setBlock", "params": [0, 0, 0, "stone"] }
```

- `method` ＝ コマンド名（**TCP ドット名直結**、§4）。
- `params` ＝ **位置引数の配列**（順序が意味を持つ）。例外として `hello` のみ object 形（§6）。
- `id` ＝ **クライアント採番の連番整数**（1 始まり・**接続単位**でリセット）。応答を id で相関させる。

### 3.2 notification（応答不要・id 省略）

```json
{ "jsonrpc": "2.0", "method": "world.setBlock", "params": [0, 0, 0, "stone"] }
```

- `id` を**省略**すると JSON-RPC の notification ＝ **応答も返らない**（高速建築でラウンドトリップを省く用途）。
- 仕様上 notification は**エラーも返らない**。b1 の `chat.post` / `world.setBlock` / `world.setBlocks` は、疎通確認と error 観測を優先して **id 付き同期 request** として扱う（§7.3、DECISIONS `2026-07-01-08`）。notification / send-only 既定化は b1 に含めず、bN / debug 統合側の後続作業とする。サーバ→クライアントの async error/log push も bN。

### 3.3 応答（サーバ → クライアント）

成功:

```json
{ "jsonrpc": "2.0", "id": 1, "result": "stone" }
```

失敗:

```json
{ "jsonrpc": "2.0", "id": 1, "error": { "code": -32000, "message": "permission_denied", "data": { ... } } }
```

- 標準 error オブジェクト `{ code, message, data? }`。予約コード（`-32700` parse / `-32600` invalid request / `-32601` method not found / `-32602` invalid params / `-32603` internal）＋サーバ定義域 `-32000..-32099`。
- 既存の名前付きエラー（`PROTOCOL_MISMATCH`・`TOKEN_EXPIRED` 等、scratch-plan §2.5 / versioning-design §8.3）は `message` ／サーバ定義コード ／ `error.data` に載せる（対応表は §7 で確定予定）。

### 3.4 id 規律

- id はクライアントが採番（1 始まりの連番、接続単位）。サーバは応答に同じ id を返す。
- クライアントは未応答要求を id キーの保留表（`_pending`）で管理し、応答到着で解決する。**接続切断時の保留解決は未実装（既知ギャップ、§9）**。

---

## 4. コマンド表（確定）

`method` は **既存 TCP プロトコルのドット名を直結**する（scratch-plan §5「既存 TCP を読み v1 の正とする」に従う）。

| method | params（位置） | 応答 | 備考 |
| --- | --- | --- | --- |
| `hello` | object（§6） | あり | 接続ハンドシェイク。1接続に1回。identity/auth/build を担う |
| `build.setWorld` | `[dimension]` | あり | build state の world/dimension を変更。`dimension` は `overworld` / `nether` / `the_end` |
| `build.setOrigin` | `[x, y, z]` | あり | build origin を変更。Scratch b1 UI は y を露出せず 0 固定で送る |
| `chat.post` | `[msg]` | あり（b1 は id 付き同期 request） / notification 時なし | チャット送信 |
| `world.setBlock` | `[x, y, z, block]` | あり（b1 は id 付き同期 request） / notification 時なし | 1ブロック設置 |
| `world.setBlocks` | `[x1, y1, z1, x2, y2, z2, block]` | あり（b1 は id 付き同期 request） / notification 時なし | 直方体充填 |
| `world.getBlock` | `[x, y, z]` | あり | ブロック取得 |
| `player.getPos` | `[]` | あり | paired player の現在 world と現在位置を stream origin 相対で返す（b2 準核） |
| `player.setPos` | `[world, x, y, z]` | あり | paired player を指定 world の stream origin 相対位置へ teleport する（b2 準核） |

- `chat.post` の message は `params[0]` の1値だけを正とする（DECISIONS `2026-07-01-01`）。
  旧テキストコマンド実装には分割された args を join して複数トークンを1メッセージ化する暗黙挙動があったが、
  JSON-RPC 21.0.0 では互換契約として保存しない。クライアントは1つの string を `[msg]` として送る。
- b1 の `chat.post` / `world.setBlock` / `world.setBlocks` は `id` 付き request として送って同期 result/error を返す（DECISIONS `2026-07-01-08`）。notification / send-only 既定化は b1 から外し、bN / debug 統合側で扱う。
- `build.setWorld` / `build.setOrigin` は protocol 21.0.0 系の b1 配布物における build model 収容条件に含める（DECISIONS `2026-07-01-10`）。API 層名は `setWorld` / `setBuildOrigin`、wire method は `build.*`。
- `world.getBlock` は **result をそのまま返す**（取得値が `undefined` / error のときは**空文字**）。戻り型の確定（int ↔ 文字列）は §7 ②。
- `player.getPos` / `player.setPos` は protocol 21.0.0 系 b2 の準核に含める（DECISIONS `2026-07-07-02`）。API 層名は `getPos` / `setPos`、wire method は `player.*`。
- `setPlayer` は**廃止**（protocol 21.0.0 系の b1 配布物でクリーン除去、DECISIONS `2026-06-15-02`/`2026-06-25-05`）。identity は `hello` が担い、サーバが token ↔ player を束縛するため**なりすまし不可**。

---

## 5. setWorld / setBuildOrigin（決定済み・b1 収容済み）

### 5.0 座標規範（確定・符号化に先行）

build コマンドの座標解釈は符号化の未定（§7④）に**先行して確定**している（DECISIONS `2026-06-25-01`/`2026-06-24-01`/`2026-06-15-04`）。両実装はこの規範を一字一句同じに実装する（食い違うと疎通で初めて露見し静かに割れる）。

- **全軸 origin 相対**：`world.setBlock`/`world.setBlocks`/`world.getBlock` の `x,y,z` は build origin からのデルタ。
- **絶対座標＝origin＋デルタ（各軸）**：とくに **絶対 y ＝ origin.y ＋ dy**。**暗黙の Y オフセットは持たない**。
- **`world_constants.y_sea` は情報定数**：hello result の `world_constants` object 内で `y_sea` として広告するのみで、**座標式に焼かない**（`2026-06-15-04` / `2026-07-02-02`）。`y_sea` は `number | null` で、`null` は不明またはその world/profile では意味を持たないことを示す。
- **既定**：build 未設定時は world=overworld・origin=(200,0,200)。
- **Scratch は y 封印**：標準 UI では `origin.y` を編集可能にしない。ただし Y を完全に隠すのではなく固定値 `0` として見せ、`setBuildOrigin` / wire `build.setOrigin` には y=0 を送る（`2026-07-02-03`）。
- **scope は stream 個別**（`2026-06-24-01`）：build state は接続（stream）ごとに保持。

> 却下＝座標規範を DECISIONS 止まりにし wire doc に書かない：ワイヤ符号化の SSOT が座標意味論を欠くと、plugin/Python が別計算をしても契約上は「合致」に見え、疎通 Layer 2 まで検出されない。符号化（§7④）と規範は別物で、規範は先に固定できる。

### 5.1 符号化（b1 収容済み）

build state を変更する `setWorld(dimension)` / `setBuildOrigin(x,y,z)` は、**両者セッション中変更可・stream 個別**で**既に確定**している（DECISIONS `2026-06-15-02` / `2026-06-24-01`）。

- **method 名＝確定（`2026-06-26-04`）**：ワイヤは **`build.*` 名前空間のドット名**＝**`build.setWorld`**(dimension)・**`build.setOrigin`**(x,y,z)。API 層の method 名は **`setWorld`/`setBuildOrigin`（camelCase）を維持**＝API 名↔ワイヤ名は別層（mcpi が既にそう、§7④）。`build.*` を `world.*` と分けるのは build state が stream 別セッション設定で共有ワールド変更ではないため。
- **params（b1）**：`build.setWorld` は `[dimension]`（`overworld` / `nether` / `the_end`）、`build.setOrigin` は `[x, y, z]`。build 未設定時は overworld・origin `(200,0,200)`。
- **Scratch b1 UI（`2026-07-01-10` / `2026-07-02-03`）**：Scratch b1 は `setWorld` / `setOrigin` を収容する。`setOrigin` の y は編集可能にせず、固定値 `0` として見せる（例: `[建築原点(X, Y, Z) を (x), 0, (z) にする]`）。X/Y/Z 編集版は標準導線に入れず、Y 軸学習は `setBlock` の y 引数に置く。

---

### 5.2 player.getPos / player.setPos（b2 準核）

`player.*` は paired player を対象にする操作群で、identity は hello/auth が確定した token に束縛された UUID から解決する。クライアントは player 名を送らない。

- **`player.getPos`**：params は `[]`。paired player の現在 world と現在位置を返す。result は `{ "world": "overworld", "pos": [x, y, z] }`。`pos` はその stream の build origin からの相対座標で、`stream.world` と player の現在 world の一致は要求しない。
- **`player.setPos`**：params は `[world, x, y, z]`。`world` を teleport 先 world とし、server が `absolute = stream.origin + [x,y,z]` を計算して paired player を移動する。player の現在 world と指定 world が異なる場合も、権限が許せば次元跨ぎ teleport として実行する。成功 result は getPos と同形の `{ "world": "...", "pos": [x, y, z] }` を返す。
- **world key**：wire/result key は hello result と揃えて `world` とする。説明上は次元（dimension）と呼んでよいが、wire key に `dimension` は作らない。
- **origin との関係**：`player.*` は stream origin を共有するが、`build.setWorld` が保持する `stream.world` には暗黙依存しない。`world.*` は `stream.world + stream.origin`、`player.*` は `explicit/current world + stream.origin` で読む。
- **権限**：許可/拒否は LuckPerms に委譲し、protocol 独自の teleport 権限体系は作らない。拒否は `permission_denied`。
- **基本 reason**：`permission_denied` / `player_offline` / `unknown_world` / `invalid_params`。エラー形は §7.3 の JSON-RPC 標準 error object と二層 reason に従う。

> 却下＝`player.getPos` を `stream.world` 不一致時 error にする案：result に現在 world を明示すれば不一致は状態でありエラーではない。却下＝`player.setPos` が暗黙に `stream.world` を使う案：world を引数で明示する方が、次元跨ぎ teleport と origin 相対の関係を説明しやすく、`getPos` の `{world,pos}` と対になる。却下＝McRemote 独自の teleport 権限を新設する案：認可体系を protocol に増やさず LuckPerms に一本化する。

---

## 6. hello ペイロード（**§6.1 / §6.5 確定・§6 全体 ratify 待ち**）

> 状態＝**部分確定**。§6.1 の要求 `params` は、`protocol` 最小・`auth:{token}` 単一モード・`build` 省略時既定・`sandbox` 非搭載で確定（DECISIONS `2026-07-04-06` / `2026-07-06-05`）。§6.5 の `auth.*` ペアリングフローも確定済み。§8 整合（`mc_version`/`supported_mc_versions` 広告の欠落）は解消済み（§6.2）、版フィールドは `v`→`protocol` に改名して §8 と一名一義化。**安定形・`protocol`=`21.0.0`・b1 は `catalogHash:null`・`world_constants.y_sea`・リッチマニフェスト再棄却は確定**（DECISIONS `2026-06-27-01`/`2026-06-27-05`/`2026-07-02-02`）。§6 全体の ratify は、証跡参照を付けた DECISIONS 追記と §6.2–§6.4 の最終整合 sweep で閉じる。

### 6.1 要求 `params`（object）

```json
{ "protocol": "21.0.0", "client": { "name": "...", "version": "...", "locale": "..." },
  "auth": { "token": "..." }, "build": { "world": "overworld", "origin": [200, 0, 200] } }
```

- `protocol` ＝ **protocol semver `21.0.0`**（§8 ネゴ用・clean な protocol 版）。**package 版 `2100.0.0b1` を載せない**（`b1` は配布チャンネル表記で互換に無関係、DECISIONS `2026-06-27-01`）。`jsonrpc` がエンベロープ版枠を占めるため版フィールドは protocol semver に一本化し、§8 の `protocol` と同名（旧称 `v` から改名・一名一義方針）。
- `sandbox` は **`hello.params` に載せない**。bridge 経由の Sandbox routing は §2 の WSS 接続メタ（例 `?sandbox=...`）が担う。直 TCP 経路では接続先 host/port が routing 情報であり、plugin が受け取る wire payload は bridge 経由でも直 TCP でも同一に保つ。
- `auth` は **`{ token }` の1モード**（token はサーバで player 束縛）。**ペアリング（token の入手）は hello の前段の独立メソッド `auth.pairBegin` / `auth.pairPoll`**（§6.5・確定 `2026-07-04-06`）＝hello 自体は pair モードを持たない。`build` 省略時は overworld・原点 (200,0,200)。
- **enforcement トグル連動**（plugin config・§10.11.1 項5）：hello の `auth` 扱いはトグルで変わる。**OFF（開発既定）**＝`auth.token` 欠落/空を許容し**無認証セッション可**（3リポ非同期着地のため・item5）＝この段では最小必須は `{ protocol }`。**ON（リリース既定）**＝`auth` 必須で、欠落→`auth_required`、検証失敗→`token_expired` / `token_revoked` / `token_not_found` / `token_invalid` 等の認証 reason（§6.3）。構文不正・未知形式・検証不能は `token_invalid`。

### 6.2 応答 `result`

```json
{
  "protocol": "21.0.0",
  "mc_version": "1.21.11",
  "supported_mc_versions": ["1.21.11"],
  "catalogHash": null,
  "world_constants": { "y_sea": 63 },
  "session": "...",
  "player": "...",
  "world": "overworld",
  "origin": [200, 0, 200],
  "permissions": { "online": true, "offline": false, "buildRange": "..." },
  "server": "..."
}
```

- **安定形（確定 `2026-06-27-05` / `2026-07-02-02`）**：hello 応答は `{protocol, mc_version, supported_mc_versions, catalogHash}`（＋session/player/world/origin/permissions）を基礎に、world/profile 情報定数だけを `world_constants` bucket に束ねる。**b1 は無認証ゆえ `catalogHash: null`**（フィールドは常在）、認証＋catalog が来る bN で実値が埋まる＝クライアントは「フィールド有無」でなく「`catalogHash` が埋まってるか」だけ見る（封筒の破壊的変更ゼロ・b2 で何が育ったか目で見える）。**入れ子リッチマニフェスト（`catalogs.block.{format,namespaces,inline,url,size}`）は再棄却**＝§7.2/§8.1 の単一 `catalogHash` 畳み込み・一名一義を維持。
- **§8 整合**：versioning-design §8.1 が要求する `mc_version` / `supported_mc_versions`（踊り場リスト）を応答に含める（§8.1 必須ゆえ省けない）。互換判定は §8 のメジャー一致則に従う。
- **`catalogHash`**（確定 `2026-06-26-03`・§7.2）：ブロック等カタログのキャッシュ識別子＝`mc_version`/`supported_mc_versions` 広告に**紐づくレジストリ指紋**（重複フィールドにしない）。クライアントは未キャッシュ時のみ本体取得（b1 は null ゆえ常に同梱既定版 fallback）。
- **`world_constants`**（確定 `2026-07-02-02`）：world/profile 依存の情報定数を束ねる object。b1 では object と `y_sea` key の存在だけを確認対象にする。wire key は `y_sea`、値は `number | null`。Python 生成定数名として `Y_SEA` を使うのは可。`y_sea` は座標式には使わず、完全な意味論、superflat 判定、full `world_constants.json` 配送、multi-version switching は bN / domain knowledge 側へ送る。

### 6.3 失敗

認証系（token 破棄＋再ペア）＝`token_expired` / `token_revoked` / `token_not_found` / `token_invalid` / `auth_required`（enforcement ON で token 欠落）。認可系（token 温存・操作のみ拒否）＝`permission_denied`。版不一致は認証系に混ぜず §8 `protocol_mismatch` に隔離。ペアリング固有の reason は §6.5。エラー形は §3.3 の JSON-RPC error オブジェクトに載せ、意味は §7.3 の二層（`code`＝`-32000`番台／`data.reason`＝小文字スネーク enum）で運ぶ。

### 6.4 確定済みの決定事項（auth 以外）

pair→token の入手フロー（§6.5）／origin 基準の相対座標／`protocol` で版交渉／権限を応答で surface／最小必須 `{ protocol }`（enforcement OFF）または `{ protocol, auth:{token} }`（enforcement ON）・build 省略時 overworld (200,0,200)。auth フロー（ペアリング）の実体は §6.5・`2026-07-04-06` で確定。Sandbox routing は hello payload ではなく §2 の bridge routing が担う。

### 6.5 認証：ペアリングフロー（確定 `2026-07-04-06`）

token の入手＝ペアリング。**hello の前段の独立メソッド `auth.*`**（hello は §6.1 の `auth:{token}` 1モードのみ）。トポロジは **poll**。完了 push は b2 では持たず（`2026-07-01-08`＝async push は bN）、bN で `auth.pairPoll` を server→client notification に差し替える＝begin 応答・`pairing_id` 相関・token payload をそのまま保存する push 形の部分集合。名前空間 `auth.*` は将来の `auth.refresh` / `auth.revoke` / `auth.logout` も同居させる。

```text
→ auth.pairBegin { token_type:"session", client:{name,version,locale}, device?:"教室PC-3" }
← { pairing_id, pair_code:"827419", expires_in:120 }
      （人間が Minecraft 内で /mcremote pair 827419 を実行）
→ auth.pairPoll { pairing_id }              ← 数秒ごとに繰り返し
← { status:"pending" }
← { status:"ok", token:"mcrs_…" }
      （失敗は error＝pair_expired / pair_not_found）
→ hello { protocol:"21.0.0", auth:{ token:"mcrs_…" }, build }
← { protocol, mc_version, …, session, player, permissions }
```

- **`auth.pairBegin`** `params`＝`token_type`（`"session"`\|`"player"`・既定 `"session"`）／`client`（`{name,version,locale}`）／`device?`（`player_token` のデバイス別発行・`last_used_at` 用ラベル）。**`protocol` は載せない**（版交渉は hello の責務・identity は版非依存で不一致は hello が弾く）。`result`＝`{ pairing_id, pair_code, expires_in }`（`pair_code`＝6桁数字・約120秒・1回限り）。
- **pair code 表示**（DECISIONS `2026-07-07-01`）：wire の `pair_code` は素6桁 ASCII のまま不変。人間向け UI は `NNN-NNN`（例 `333-333`）で表示し、コピー対象はコマンド全体 `/mcremote pair NNN-NNN` を既定にする。plugin の `/mcremote pair` 入力は区切りとして入り得る非数字（`-`・空白等）を除去し、残りが ASCII 数字 `0-9` の6桁である場合だけ bind する（全角数字は変換しない）。これは表示・人間入力の規約であり、`auth.pairPoll` は引き続き `pairing_id` 相関で wire に `pair_code` を戻さない。
- **相関の分離**：`pair_code` は**人間が `/mcremote pair <code>` で打つ秘密**、`pairing_id` は**wire 相関子**。plugin が `pair_code → pending(pairing_id)` を保持し、`/mcremote pair` 実行者の UUID を pending に束縛する（正本＝plugin・bridge は透明中継）。
- **`auth.pairPoll`** `params`＝`{ pairing_id }`。`result`＝`{ status:"pending" }` または **`{ status:"ok", token }`（最小）**。**`pending` は error でなく `result.status`**（待機は失敗でない）。失敗は error＝`pair_expired`（code TTL 経過）／`pair_not_found`（不正な `pairing_id`）。token は**要求した1種のみ**発行（`session_token`/`player_token` を同時発行しない）。
- **単一ソース原則**：`pairPoll` の `ok` は **token だけ**返す。`player`(UUID)・`permissions`・`world`・`origin` は**続く hello の `result` が単一ソース**（§6.2）＝pairPoll に冗長フィールドを持たせない。`token_type` も prefix（`mcrs_`/`mcrp_`）と要求から自明ゆえ返さない。WireScope（#13）は権限・world を hello から読む。
- **bridge 透明性**：poll は `pairing_id` で相関するため、`pairBegin`↔`pairPoll` で同一 TCP 接続を保持する必要がない（sticky TCP 不要・bridge は各 request を素通しできる）。ただし Sandbox route は WSS 接続メタとして bridge 側が保持する（§2）。plugin 側 TCP が `auth_required` / 認証系 reason の後で閉じても、同一 browser-side session の `auth.*` と再 `hello` は同じ Sandbox へ送る。
- **token 種別**（scratch-plan §2.5）：`session_token`（`mcrs_`・約2h・Scratch/一時利用）／`player_token`（`mcrp_`・長期・デバイス別・CLI `login`）。Scratchの標準導線はsessionのみ、Pythonは永続store / list / revoke完成後にplayerを既定とする。サーバはhashのみ保存し、認可は常にUUID→LuckPerms。
- **credential scope**：tokenはopaqueなままとし、channel / Sandbox名をwire tokenへencodeしない。serverごとのcredential storeが未知tokenを拒否し、client storeはcredentialを接続先profile / targetへ紐づけて別channel・別Sandboxへ黙って送らない。将来複数serverがcredential storeを共有する場合だけ、明示的なaudience / scopeをprotocol ratifyする。
- **PoPは未批准**：公開鍵付きpairing、challenge / nonce、proof、signature errorは現protocolへ追加しない。接続時Proof of Possessionはtoken文字列だけの別端末再利用を抑えるhardening候補だが、b4 / rc / public betaのgateから外した（DECISIONS `2026-07-16-03`）。採用判断までalgorithm、key encoding、canonical bytes、challenge wire shapeを推測で固定しない。Bridgeは採用後もpayload-transparentであるべきだが、これは現時点のwire契約追加ではない。
- **クライアント契約（reason 駆動・OFF/ON 統一）**：クライアントは**まず `hello`（token を持てば載せる）を試み、`auth_required` が返ったときだけ**本フロー（`pairBegin`→`pairPoll`→再 `hello`）に入る。この1経路が OFF/ON/token 失効を統一する＝**enforcement OFF（開発既定）では token 無し hello が成功し `auth_required` が返らない＝ペアリングは自動的にスキップ**（dev 動線に別コードパス不要・§6.1・item5）。ON では token 欠落時に `auth_required`、token 検証失敗時に §6.3 の認証系 reason が返る。認証系 reason で token を破棄したら同じく先頭（hello 試行）へ戻る。
- **非規範（クライアント実装の目安・ratify 対象外）**：poll 間隔 ≈1–2s、poll の timeout は `pairBegin` が返す `expires_in`（`pair_code` TTL・≈120s）で、超過は `pair_expired` として扱う。`pairing_id` はクライアント in-memory 保持でよい（リロードで破棄＝ユーザーは接続ブロックを再実行）。

---

## 7. 未確定（要決定）

| # | 論点 | 状態 |
| --- | --- | --- |
| ① | **block id 表現**（文字列名・名前空間） | **確定** `2026-06-26-03`（§7.1） |
| ② | **`world.getBlock` 戻り型** | **確定** `2026-06-26-03`（文字列カタログ名・§7.1） |
| ③ | **notification のエラー方針** | **b1 スコープ確定** `2026-07-01-08`（`2026-06-27-04` / `2026-07-01-06` を改訂）。b1 の setBlock/setBlocks/chat.post は **id 付き同期 request** として扱い、疎通確認・error 観測を優先する。notification / send-only 既定化とサーバ→クライアント async error/log push は b1 に含めず **bN / debug 統合**へ送る。残: async push の設計は debug 統合と同時 |
| ④ | **命名系統** | **確定** `2026-06-26-04`。ワイヤ method はドット名前空間（build setter は `build.*`＝`build.setWorld`/`build.setOrigin`）・API 名は camelCase 維持（§5.1）。b1 params は §5.1 |
| ⑤ | **権限既定値** | 未決（**plugin/LuckPerms の現実依存**）。hello 応答 `permissions` の既定は config.yml の権限名（`mcr.online`/`mcr.offline`/`mcr.build.range`、scratch-plan §2.5）と実 LuckPerms 既定に律速＝plugin b1/認証 bN で実値を確認して確定 |

> §8 のエラーコード（`PROTOCOL_MISMATCH` 等）と認証系コード（`TOKEN_EXPIRED` 等、scratch-plan §2.5）を JSON-RPC error オブジェクトへどう写像するかの対応表も、ここで確定する。

### 7.1 block_state_ref（確定 `2026-06-26-03`、`2026-06-27-02` で改訂）

§7①② への回答。block 値は単なる id ではなく **state 込みの `block_state_ref` 文字列**＝正準形は `namespace:path` または `namespace:path[prop=value,...]`。**1ルール「入力 tolerate・出力 canonical-full」を namespace と state の両軸に適用する**（`2026-06-27-02`）。

- **基本形＝文字列名**（平坦化後＝1.13+ の1系統）。数値 id+data・mcpi は先送り（mc-constants #11 整合）。
- **入力（tolerate）**：
  - namespace＝無印 OK。plugin が `:` 無し→`minecraft:` を補完（チャットコマンド/mcpi と同様）。**無印の未知名は失敗扱い**（黙殺しない、§7.3 `unknown_block`）。
  - state＝部分指定 OK・順不同 OK。未指定 prop は plugin の `createBlockData` が default 補完。素の id（全 default）も可。
- **出力＝正準（canonical-full）**：getBlock は常に **(1) 完全修飾**（バニラも `minecraft:…`・`2026-06-27-02` で旧「バニラ短縮」を訂正）**(2) full state**（全 prop 明示）**(3) プロパティ名アルファベット昇順**（plugin が `getAsString()` 出力をソート＝Paper の emit 順は未規定で版で崩れうるため我々の契約で固定し、往復テストを exact 文字列で書けるようにする）。**int 廃止方向**。
- **値の表記**：bool は小文字 `true`/`false`、整数 state（`level`/`age` 等）は裸の数字。
- **変換責務＝pass-through**：文字列名を client→bridge→plugin で素通し。**数値変換は導入しない**（mcpi 統合時に別設計）。
- **round-trip**：正準（完全修飾＋full＋ソート）形で**文字列等価**が成立。例 `setBlock(...,"oak_stairs[facing=north]")`（部分・無印）→ `getBlock(...) → "minecraft:oak_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]"`（完全修飾・full・ソート済み）。テストは full 形を assert（意味的 round-trip）。
- **層の分離**：短縮名・state 省略・kwargs などの書きやすさ/見やすさは **UI・教材・Python 定数の入力側**で吸収（`2026-06-27-02`）。catalog の `default_state` が「短い表示↔full 復元」の前提＝§7.2 と連動（catalog 本体は b2）。

### 7.2 カタログ配送・キャッシュ（確定 `2026-06-26-03`）

§7①の単一ソース（versioning-design `2026-06-15-04`）の具体化。状態＝**確定**。

- **単一ソース**＝サーバ稼働中レジストリ（ロード済み mod 含む）から block/entity/particle を生成。Python 定数／Scratch プルダウン／実配置先を一致させる。
- **配送＝認証後**：hello 応答が `catalogHash` を返し、クライアントは**未キャッシュ時のみ**本体取得。
- **キャッシュキー＝`catalogHash`**（版＋mod レジストリ指紋）。
- **ローカル（Python）＝PC グローバルキャッシュ**（`~/.cache/mc-remote/` 等・言語/プロジェクト横断共有）。project-root の定数ファイルはその生成物。**モジュールは既定版のみ同梱**（全版 pack 取りやめ・他版は接続時にグローバルキャッシュへ充填）。
- **クラウド（Scratch）＝IndexedDB**（オリジン単位・catalogHash キー）＋同梱既定版フォールバック（FS 不可のため）。
- **§8 整合**：hello のカタログ版識別子は §8.1 がサーバに要求する `mc_version`/`supported_mc_versions` 広告と**一名一義に統合**（重複フィールドを作らない）。`catalogHash` はそれに紐づくレジストリ指紋（§6.2）。
- 前提：「未接続で任意版オフライン切替」は要件から落とす。

### 7.3 エラー設計（確定 `2026-06-27-03`、`2026-07-01-08` で改訂、`2026-07-07-02` で b2 player reason を追加）

§7③ の b1 部分を画定。**JSON-RPC 標準 error オブジェクトに一本化**（独自封筒を作らない＝`2026-06-26-01` の標準枠原則に忠実）。`code` は JSON-RPC 標準に従い、**意味は `data.reason`（安定 enum）が運ぶ二層**。UI/AI/test は `reason` を分岐 key にし family（code）を意識しなくてよい。

- **`message`**＝英語短文（ja は client が `reason` から投影）。
- **`data.ref`**＝問題の入力をエコー（**必須**）。
- **`data.allowed`**＝`invalid_property_value` で許容値を返せれば返す（**b1 任意 / b2 必須**・catalog 連動）。

| family | code | reason | 意味 | b1 |
| --- | --- | --- | --- | --- |
| ref 検証 | `-32602`（Invalid params） | `malformed_ref` | 括弧崩れ等の parse 失敗 | ○ |
| | | `unknown_block` | 文法 OK・block 不在（無印補完後の未知名含む） | ○ |
| | | `unknown_property` | prop 名がそのブロックに無い（`stone[axis=y]`） | ○ |
| | | `invalid_property_value` | 値が許容外（`oak_log[axis=w]`）。`allowed` を返せる | ○ |
| params 検証 | `-32602`（Invalid params） | `invalid_params` | JSON-RPC params の形・型・座標値が不正 | b2 |
| | | `unknown_world` | 指定 world が解決できない | b2 |
| world-state | `-32000`番台（実装定義域） | `build_denied` | build policy / 範囲 / 認可により操作拒否。返せる場合は `data.bounds` / `data.violating` 等で理由を補足 | ○ |
| player-state | `-32000`番台（実装定義域） | `permission_denied` | LuckPerms 等の認可により操作拒否。token は温存 | b2 |
| | | `player_offline` | token は有効だが paired player がオンラインでない | b2 |

- **`missing_namespace` は廃止**（無印は有効＝`2026-06-27-02`、`minecraft:` 補完される）。
- **reason 分割の理由**：生徒のミスが別物（付け忘れ/構文破壊/prop 無い/値不正）で、ライブ画面が別メッセージを出せると切り分け教育になる。`allowed` を返せるのは `invalid_property_value` だけ＝非対称が綺麗に出る。
- **`unloaded_chunk` は b1 reason から廃止**（DECISIONS `2026-07-01-08`）。未生成 chunk に対してロード/生成せず有意味な block 操作や query を行う実体はなく、許可された操作ならロード/生成して処理する。禁止すべき操作は chunk ロード状態ではなく build policy / 範囲 / 認可の問題なので、ユーザーに返す安定 reason は `build_denied` とする。chunk generation policy が必要になった場合は bN で別 reason として設計する。
- **後送り（名前予約のみ）**：`catalog_cache_stale`・`unknown_namespace`・`out_of_bounds`(world-state/y 範囲外・即判定で混乱しないため後送り)。
- **適用範囲**：b1 では getBlock に加え、chat.post/setBlock/setBlocks も **id 付き同期 request** として result/error を取れる形を基準にする（`2026-07-01-08`）。notification は JSON-RPC 上は可能だが result/error を返さないため、send-only 既定化は b1 の疎通確認対象から外す。async push は bN。
- **送信モードの体験タクソノミー**（`visible`/`paced`・`async`・`sync`・`batch`/`job`）は wire でなく**体験設計の層**＝DECISIONS `2026-07-01-08` が持つ。wire 上の実体は notification（応答なし）と id 付き request（同期 result/error）の2系統だけ。b1 は後者を確認基準にし、send-only / async UX は bN / debug 統合側で設計する。`visible`/`paced` はクライアント側 pacing、`batch`/`job` は高水準 API・後続プロトコルの話。

---

## 8. 採用判断：JSON-RPC 2.0（却下した独自最小形）

DECISIONS `2026-06-26-01` で確定。**実装済みの独自最小形 `{id?,cmd,args}` / `{id,result|error}` から JSON-RPC 2.0 へ寄せた**。

### 8.1 なぜ JSON-RPC 2.0 か

- **概念がほぼ 1:1**：`cmd`→`method`・`args`→`params`（位置配列のまま）・`id` 省略=notification・`{id,result|error}`。寄せる調整は「定数 `jsonrpc:"2.0"` 追加＋フィールド改名＋標準 error 形採用」で、**意味論の再設計が不要**。
- **開いた論点が閉じる**：標準 error オブジェクト `{code,message,data}` が §7 ③（send-only エラー通知）とエラー形未定を埋める。自前でエラー形を設計しなくてよい。
- **多言語クライアント計画への適合**（versioning-design `2026-06-25-04` 非対称成熟 / §10.13）：Java/JS/Rust 等の各クライアントが JSON-RPC ライブラリを既製で使え、各自が独自エンベロープを手書きしない。
- **最安の瞬間**：b1（`2100.0.0b1`）は plugin/python 両側で実装中（NOTES `2026-06-25-05` 降ろし済み）。凍結済みプロトコルの作り直しではなく「独自形で書く代わりに JSON-RPC で書く」だけなので、整合を取る最も安いタイミング。
- **版レイヤの分離**：`jsonrpc:"2.0"` がエンベロープ形式版を自己記述するため、hello の版フィールドは protocol semver（§8）に一本化でき、版概念の二重化を避けられる。

### 8.2 却下：独自最小形のまま pin

- 利点は1メッセージ約30バイト軽い・目視がわずかに簡素な点のみ（wss では誤差）。
- 代償：JSON-RPC を採らない理由を別途記録し、**エラーオブジェクト（§7 ③）を自前設計**し、**各言語クライアントが独自エンベロープを再実装**する。利得 < 損失。

### 8.3 注意（エンベロープ非依存）

notification のエラー方針（§7 ③）は**エンベロープ選択に関わらず残る設計判断**。JSON-RPC はそれを標準の枠（notification＝無応答／error オブジェクト）で綺麗に表現するだけで、論点自体を消すわけではない。

---

## 9. 既知ギャップ（実装 TODO・堅牢性）

- **WS close 時の保留解決（§3.4）**：クライアントは未応答要求を id キーの保留表（`_pending`）で管理するが、**接続切断時に `_pending` を reject していない**＝`world.getBlock` 等の応答待ちが接続断で**ハングし得る**。v1 で timeout / close-reject を規定するか、実装 TODO 止まりかは要決定（13-scratch-client の既知ギャップ、scratch-plan §4.1）。
- **Scratch の `setOrigin` UI は b1 最小形（§5.1）**：Scratch b1 は `setWorld` / `setOrigin` を収容するが、`setOrigin` の y は編集可能にせず固定値 `0` として見せ、0 固定で送る。X/Y/Z 編集版は標準導線に入れない。session/reconnect/save と origin 固定タイミングの厳密仕様は未決で、b1 release gate の blocker ではない（DECISIONS `2026-07-01-10` / `2026-07-02-03`）。

---

## 10. b1 到達点（疎通テスト）

b1（protocol は clean な 21.0.0、配布物は `2100.0.0b1` 系）は **payload flip と疎通確認に徹し MVP を小さく切る**（versioning-design §10.11、DECISIONS `2026-06-25-05` / `2026-07-01-08`）。エラー往復は **id 付き request**（setBlock/setBlocks/chat.post の同期 result/error）または **getBlock**（常に request）で示す。send-only / notification 既定化は b1 の到達点に含めず、bN / debug 統合へ送る。

**b1 で通したい最小テスト:**

1. `hello` が成功する（安定応答・`protocol`=`21.0.0`・`catalogHash:null`・`world_constants.y_sea` key が存在、§6）。
2. `build.setWorld` / `build.setOrigin` が収容されている（Scratch b1 UI の `setOrigin` は固定値 `0` を見せ、y=0 固定で送る）。
3. `world.setBlock(..., "minecraft:stone")` が成功する。
4. `world.setBlock(..., "minecraft:oak_log[axis=y]")` が成功する。
5. `world.getBlock(...)` が full・完全修飾の `"minecraft:oak_log[axis=y]"` を返す（§7.1 正準形）。
6. 不正 state・未知 block は id 付き setBlock/setBlocks で、build policy 範囲外は id 付き setBlock/setBlocks または getBlock で、対応する `data.reason`（`unknown_block` / `invalid_property_value` / `build_denied` 等、§7.3）の error が返る。

**b1 でやらないこと**（意識的に bN へ送る）：全 block catalog 配信 / mod catalog 取得 / full `world_constants.json` 配送 / `y_sea` の完全な意味論・superflat 判定・multi-version switching / Scratch 全 state UI / Scratch `setOrigin` の X/Y/Z 編集版・session/reconnect/save と origin 固定タイミングの厳密仕様 / Python 完全補完・`.pyi` 生成 / creative tab 再現 / ドア helper 実装 / kwargs 入力（catalog 連動・b2）/ サーバ→クライアント async error push（debug 統合・bN）。
