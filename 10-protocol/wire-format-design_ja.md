# 設計記録: McRemote ワイヤ形式（JSON-RPC 2.0 エンベロープ）

> マイクラリモコン（Code2CreateClub / mc-remote.com）設計記録
> 関連: `Naohiro2g/McRemote`（プラグイン）, `Naohiro2g/minecraft-remote-api`（API）, `Naohiro2g/scratch-editor`（Scratch クライアント）
> 出典: scratch-editor 作業セッション 2026-06-26（`scratch3_mcremote/index.js` の DRAFT 実装でピン留め）
> 結節点: [versioning-design] §3（メジャー増分）/§8（hello ネゴ）/§10.11（protocol 21.0.0／22.0.0／23.0.0）と直結。本文書は**ワイヤ符号化の SSOT**で、版判定規則の正は versioning-design §8。

---

## 1. 位置づけ（protocol semver との関係・用語の整理）

本文書は**プラグイン ↔ 各クライアントの実際のワイヤ符号化**（フレーミング・エンベロープ・コマンド表・エラー形）を定める。これは [versioning-design] が扱う **protocol semver（20.0.0 / 21.0.0…）とは別レイヤ**。

- **エンベロープ形式版** ＝ `jsonrpc: "2.0"`（JSON-RPC 2.0 を採用、§3）。各メッセージに自己記述で載る。
- **protocol 版** ＝ semver（例 **`21.0.0`／`22.0.0`／`23.0.0`**）。互換判定は versioning-design §8（メジャー一致必須・`plugin.minor >= client.minor`・パッチ不問）。hello で交渉する。**package 版 `2100.0.0b1`／`2200.0.0b5`／`2300.0.0b6` とは別レイヤ**＝`bN` は配布チャンネル表記で **wire 非搭載**、hello の`protocol`にはcleanなprotocol semverを載せる（DECISIONS `2026-06-27-01`／`2026-08-19-02`／`2026-08-26-06`）。packageはprotocolからfold規則（versioning-design `2026-06-19-04`）で派生＝独立ではない。

> **「protocol v1」という旧称について**：scratch-plan §4/§5 が「プロトコル v1 仕様書」と呼んでいたのは本文書のワイヤ仕様のこと。protocol semver の `1.x` とは無関係で混同しやすいので、本リポでは「**ワイヤ形式**」と呼び、semver は versioning-design の番号で呼ぶ。このワイヤ符号化が初めて載ったprotocol semverは **21.0.0**、構造化block valueへの破壊的変更は **22.0.0**、`block_right_click`から`pickaxe_poke`への破壊的置換は **23.0.0** に載る。配布物側の`bN`はprotocol自体のbetaではない（versioning-design §10.11）。

---

## 2. トランスポートとフレーミング

トランスポートは**経路で2系統**ある。ブラウザ（Scratch）は混在コンテンツ制約から wss が必須（DECISIONS `2026-06-11-01`、外部事実 `F-loopback`）、Python は bridge を介さず直 TCP（`Minecraft.create()` が独立 socket）。bridge が wss ⇔ TCP を透過変換するため、プラグインから見れば bridge 経由の Scratch も直 TCP の Python も同等。

- **経路別フレーミング**（DECISIONS `2026-06-26-02`）：
  - **wss 経路**（ブラウザ/Scratch、bridge 経由）＝**1 WS メッセージ ＝ 1 JSON**。WS がメッセージ境界を持つため改行区切りは不要で、1 メッセージに複数 JSON を連結しない。
  - **直 TCP 経路**（Python クライアント／bridge→プラグインのホップ）＝**改行区切り（1行=1 JSON・`\n` 終端）**。TCP はバイト列で境界を持たないため枠が必須。**改行区切りは検証済み（2026-06-26、現 TCP read ループ）で、mcpi テキスト→JSON-RPC の payload 差し替えを跨いで不変**。JSON 化後は **compact 直列化を強制**し JSON 内部に生改行を出さない。bridge は WS 1 メッセージを 1 行に詰めて TCP へ流す。
- **bridge routing**（DECISIONS `2026-07-06-05`）：wss 経路の接続先 Sandbox は JSON-RPC payload ではなく WSS 接続メタで指定する。既定形は `wss://bridge.mc-remote.com/?sandbox=sb-dev.mc-remote.com`。bridge は `sandbox` を allowlist で検証し、該当 Sandbox へ TCP を張る。**WSS session は route context の寿命、bridge→plugin の TCP connection は一時 transport** とする。plugin 側 TCP close は browser 側 WSS close を必ずしも意味しない。bridge は JSON-RPC error reason を解釈して WSS 維持/切断を分岐せず、次の WS message が来たら同じ route context で再 dial できる。`auth_required` 等で plugin 側 TCP が閉じても、続く `auth.*` と再 `hello` を同じ Sandbox へ流す。直 TCP 経路では接続先 host/port 自体が route であり、wire payload には載せない。
  **Bridge 共有の単位はクラスタ単位で決める**（`2026-07-30-03`）：同一セッション内で複数の接続先を行き来（比較・切替）させたい場合だけ共有 Bridge＋複数 Sandbox の allowlist を使う。開発時の variation 比較を確実に分離したい場合や、学校のクラス別・部活別・イベント別のサーバー／ワールドを確実に分離したい場合は、各環境が独立した Bridge・単一 Sandbox を持つ。Bridge 自体は environment 固有の state を持たない中継層であり、比較・切替を必要としない環境同士で Bridge を共有すると、1つの障害・設定ミスが無関係な環境の公開到達性を道連れにする。
- **非 JSON のメッセージ／行は破棄**。**未知の `id` を持つ応答も破棄**（id 相関で待ち先が無いもの）。両経路で共通。

> 検証済み（2026-06-26、両側実装）：直 TCP の境界は改行区切りで plugin/Python が一致＝Python `minecraft-remote-api`（branch `protocol-21.0.0-b1`、`mc_remote/connection.py` は送信時 `\n` 付与・受信 `readline().rstrip("\n")`）／plugin `McRemote`（`RemoteSession.java` の `BufferedReader.readLine()`）。既存の行指向プロトコルと地続き。
> **live-state（2026-06-26）**：現 TCP payload は旧 mcpi テキスト（`world.getBlock(x,y,z)`・カンマ区切り応答）で、JSON-RPC エンベロープ（§3・`2026-06-26-01`）は **TCP 経路に未着地**＝b1 残作業（フレーミング不変・payload のみ差し替え）。`connection.py`/`RemoteSession.java` を**同時に flip する原子操作**＝hello が新規で中間相互運用形が無いため、片側だけ差し替えると改行枠は生きてもパースが割れる。回帰ベースライン（差し替え前 mcpi 経路）を取ってから flip し、hello 疎通（Layer 1）を差し替え対称性の最初の証明とする（捕捉: NOTES 2026-06-26 横断）。

---

## 3. エンベロープ（JSON-RPC 2.0）

JSON-RPC 2.0 を採用する（採用判断と却下案は §8）。

### 3.1 要求（クライアント → サーバ）

```json
{ "jsonrpc": "2.0", "id": 1, "method": "world.setBlock", "params": [0, 0, 0, { "block_id": "minecraft:stone", "state": {} }] }
```

この例はprotocol 22の形である。protocol 21の文字列block refは§7.1の改訂前履歴として扱う。

- `method` ＝ コマンド名（**TCP ドット名直結**、§4）。
- `params` ＝ **位置引数の配列**（順序が意味を持つ）。例外として `hello` のみ object 形（§6）。
- `id` ＝ **クライアント採番の連番整数**（1 始まり・**接続単位**でリセット）。応答を id で相関させる。

### 3.2 notification（応答不要・id 省略）

```json
{ "jsonrpc": "2.0", "method": "world.setBlock", "params": [0, 0, 0, { "block_id": "minecraft:stone", "state": {} }] }
```

- `id` を**省略**すると JSON-RPC の notification ＝ **応答も返らない**（高速建築でラウンドトリップを省く用途）。
- 仕様上 notification は**エラーも返らない**。b1 の `chat.post` / `world.setBlock` / `world.setBlocks` は、疎通確認と error 観測を優先して **id 付き同期 request** として扱った（§7.3、DECISIONS `2026-07-01-08`）。protocol 22／b5では`world.setBlock`／`world.setBlocks`に限り、DEBUG／TRACEはid付きrequest、FASTはnotificationを使う（`2026-08-20-03`）。server pushは`2026-08-16-05`で採らず、eventは`events.poll`、command errorは対応requestで観察する。

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

### 3.5 build execution modeと`connection.flush`

protocol 22／b5のclientは、`world.setBlock`／`world.setBlocks`だけにDEBUG／TRACE／FASTを投影する。
mode名とTRACE delayはstream-scopedなclient execution policyであり、wire params、hello、plugin build stateへ
送らない。

| mode | wire | 呼出元の待機 |
| --- | --- | --- |
| DEBUG | id付きrequest | server responseまで待つ |
| TRACE | id付きrequest | server responseまで待ち、成功後にclient側delay |
| FAST | idなしnotification | 個別responseを待たず、通常は送信列への登録後に継続 |

TRACEの既定delayは`0.25`秒、許容範囲は有限な`0`〜`2.0`秒（両端を含む）で、成功した一回の
setter呼出しごとに呼出元だけを待たせる。範囲外をclampせず、mode変更前に拒否して旧mode／delayを維持する。
`setBlocks`の領域内blockごとには待たない。error時は待たない。FASTもfinite bufferとtransport
backpressureには従う。

`connection.flush`は、同一connectionの送信列で先に登録されたcommandが成功または拒否の終端へ到達するまで
待つ明示barrierである。integer idを持つrequest、exact `params: []`、authenticated hello後だけを正規形とし、
`result: null`を返す。build origin／construction permissionを要求せず、work budgetを消費しない。idなし呼出しは
responseを持たず完了保証を与えない。

flush成功は個々のnotification成功を集約しない。Paper main thread上のMcRemote handlerと必要なPaper API呼出しが
終わり、後続McRemote操作が状態を観察できる時点までを保証する。chunk永続保存、Minecraft client描画、後続tickの
物理収束、他connectionからの後続変更は保証しない。同一connectionの後続requestもFIFO上はordering pointになるが、
worldを観察しない明示barrierは`connection.flush`とする。

clientは`connection.flush`だけの別magic timeoutを作らず、同じconnectionの通常request timeoutを適用する。
timeoutはserverから返されたJSON-RPC errorではなく、先行commandの成功／拒否を確定できないlocalな完了不明である。
非冪等操作を自動retryせず、mode切替を成立させず、当該connectionを回収する。candidateのtimeout実値はclient fixture／
lockへ記録し、b8実装後・API freeze前の負荷較正でruntime policyとして更新できる。

---

## 4. コマンド表（確定）

`method` は **既存 TCP プロトコルのドット名を直結**する（scratch-plan §5「既存 TCP を読み v1 の正とする」に従う）。

| method | params（位置） | 応答 | 備考 |
| --- | --- | --- | --- |
| `hello` | object（§6） | あり | 接続ハンドシェイク。1接続に1回。identity/auth/build を担う |
| `build.setDimension` | `[dimension_ref]` | `{dimension,origin}` | protocol 22のstream-local DimensionKeyを変更（§5.1） |
| `build.setOrigin` | `[x, y, z]` | `{dimension,origin}` | build originを変更し、server正準build contextを返す |
| `chat.post` | `[msg]` | あり（b1 は id 付き同期 request） / notification 時なし | チャット送信 |
| `world.setBlock` | `[x, y, z, blockSpec]` | id付きは`null` / notification時なし | protocol 22では構造化`BlockSpec`で1ブロック設置（§7.1） |
| `world.setBlocks` | `[x1, y1, z1, x2, y2, z2, blockSpec]` | id付きは`null` / notification時なし | protocol 22では構造化`BlockSpec`で直方体充填（§7.1） |
| `world.getBlock` | `[x, y, z]` | あり | protocol 22では構造化`BlockValue`を返す（§7.1） |
| `world.getBlocks` | `[x1, y1, z1, x2, y2, z2]` | `BlockValue[]` | protocol 22の有界領域query（§7.1.1） |
| `connection.flush` | `[]` | `null` | 同一connectionの先行commandに対する明示barrier（§3.5） |
| `catalog.get` | `[]` | あり | 稼働中 registry から block/entity/particle catalog を取得（b3 実装予定、§7.2.1） |
| `player.getPos` | `[]` | あり | paired playerの現在dimensionと現在位置をstream origin相対で返す（§5.2） |
| `player.setPos` | `[dimension_ref, x, y, z]` | あり | paired playerを指定dimensionのstream origin相対位置へteleportする（§5.2） |
| `player.getPose` | `[]` | あり | paired playerの現在dimension・位置・向きをstream origin相対で返す（§5.3） |
| `player.setPose` | `[dimension_ref, x, y, z, yaw, pitch]` | あり | 指定dimensionへ位置・向きを1回のteleportで一体反映する（§5.3） |
| `events.poll` | `[after_sequence]`／`[after_sequence, {max_events}]` | あり | epoch-scoped event ringを非破壊取得。filterは条件付きb9以降のcandidate（§5.4） |
| `events.clear` | 後続contractで固定 | あり | retained eventの明示破棄候補。条件付きb9以降（§5.4） |
| `world.getHeight` | `[x, z]`または`[x, z, max_y]` | あり | origin相対の最上面block高を返す（b5、§5.6） |
| `world.spawnParticle` | `[x, y, z, offset_x, offset_y, offset_z, particle, speed, count, (force)]` | あり | 9／10 params、`force`省略時`true`。b5はdata不要particleのみ（§5.7） |
| `world.spawnEntity` | `[x, y, z, entity]` | あり | entityを生成しepoch-scoped handleを返す（b5、§5.7） |
| `player.getDirection` | b7 contractで固定 | あり | paired playerの向きを単位vectorで返すcandidate（b7、§5.8） |
| `player.setDirection` | b7 contractで固定 | あり | 非zero vectorを向きへ正規化して適用するcandidate（b7、§5.8） |
| `entity.getDirection` | b7 contractで固定 | あり | handle対象の向きを単位vectorで返すcandidate（b7、§5.8） |
| `entity.setDirection` | b7 contractで固定 | あり | 非zero vectorをhandle対象の向きへ適用するcandidate（b7、§5.8） |
| `world.getNearbyEntities` | b8 contractで固定 | あり | boundedな近傍entity検索。playerを除外（b8、§5.8） |
| `entity.getPose` | b8 contractで固定 | あり | handle対象のposeを返す（b8、§5.8） |
| `entity.setPose` | b8 contractで固定 | あり | handle対象のposeを一体更新（b8、§5.8） |
| `entity.remove` | b8 contractで固定 | あり | entityを除去しhandleを即時失効（b8、§5.8） |
| `world.getSign` | `[x, y, z]` | `{front:[LineValue×4],back:[LineValue×4],waxed:bool}` | signの両面とwaxedを正準形で取得（b6、§5.8.1） |
| `world.setSign` | `[x, y, z, {front?:[LineSpec×4],back?:[LineSpec×4]}]` | `null` | 指定面を面内no-mergeの厳密4行へ置換（b6、§5.8.1） |
| `world.updateSignLine` | `[x, y, z, face, line_index, LineSpec]` | `null` | signの一面・一行だけをPATCH（b6、§5.8.1） |

- `chat.post` の message は `params[0]` の1値だけを正とする（DECISIONS `2026-07-01-01`）。
  旧テキストコマンド実装には分割された args を join して複数トークンを1メッセージ化する暗黙挙動があったが、
  JSON-RPC 21.0.0 では互換契約として保存しない。クライアントは1つの string を `[msg]` として送る。
- b1 の `chat.post` / `world.setBlock` / `world.setBlocks` は `id` 付き request として送って同期 result/error を返した（DECISIONS `2026-07-01-08`）。protocol 22／b5はset系だけにconnection単位のDEBUG／TRACE／FASTを導入し、`chat.post`へ暗黙拡張しない（`2026-08-20-03`）。
- protocol 22は`build.setDimension`／`build.setOrigin`を使う。protocol 21の`build.setWorld`／`setWorld()`はb4以前の履歴で、alias／unionを作らない（`2026-08-22-02`）。
- `world.getBlock` はprotocol 22で`BlockValue`をresultとして返す。失敗を空文字へ畳まずJSON-RPC errorで返す（§7.1／§7.3）。protocol 21の文字列resultはb4までの履歴である。
- `catalog.get` は protocol 21.0.0 系 b3 の実装予定に含める（DECISIONS `2026-07-29-04`、§7.2.1）。API 層名・wire method とも `catalog.get`。認証後のみ有効で、稼働中 registry から block/entity/particle を単一 response で返す。
- `player.getPos` / `player.setPos` は protocol 21.0.0 系 b2 の準核に含める（DECISIONS `2026-07-07-02`）。API 層名は `getPos` / `setPos`、wire method は `player.*`。
- `player.getPose` / `player.setPose` は protocol 21.0.0 系 b4 の実装予定に含める（DECISIONS `2026-07-29-03`、§5.3）。API 層名は `getPose` / `setPose`、wire method は `player.*`。既存 `getPos` / `setPos` は廃止せず維持する。
- b5の`events.*`／`world.*`はprotocol 22.0.0／artifact b5、b6の追加`world.*`／`entity.*`／eventはprotocol 23.0.0／artifact b6のcompatibility setとして実装する。b6は`block_right_click`を削除して`pickaxe_poke`へ置換し、それ以外のb5 contractをcarryする（DECISIONS `2026-08-16-04`〜`07`、`2026-08-19-02`、`2026-08-26-06`、§5.4〜§5.8）。
- `auth.*`（`auth.pairBegin` / `auth.pairPoll` / `auth.listCredentials` / `auth.revoke` / `auth.logout`）は hello の前段に位置する認証・credential 管理の名前空間で、**本表ではなく §6.5 / §6.6 が正本**。ペアリングは §6.5、credential の一覧と失効は §6.6（`2026-08-02-01`）。
- `setPlayer` は**廃止**（protocol 21.0.0 系の b1 配布物でクリーン除去、DECISIONS `2026-06-15-02`/`2026-06-25-05`）。identity は `hello` が担い、サーバが token ↔ player を束縛するため**なりすまし不可**。

---

## 5. DimensionKey / build context

### 5.0 座標規範（確定・符号化に先行）

build コマンドの座標解釈は符号化の未定（§7④）に**先行して確定**している（DECISIONS `2026-06-25-01`/`2026-06-24-01`/`2026-06-15-04`）。両実装はこの規範を一字一句同じに実装する（食い違うと疎通で初めて露見し静かに割れる）。

- **全軸 origin 相対**：`world.setBlock`/`world.setBlocks`/`world.getBlock`/`world.getBlocks` の `x,y,z` は build origin からのデルタ。
- **絶対座標＝origin＋デルタ（各軸）**：とくに **絶対 y ＝ origin.y ＋ dy**。**暗黙の Y オフセットは持たない**。
- **`world_constants.y_sea` は情報定数**：hello result の `world_constants` object 内で `y_sea` として広告するのみで、**座標式に焼かない**（`2026-06-15-04` / `2026-07-02-02`）。`y_sea` は `number | null` で、`null` は不明またはその world/profile では意味を持たないことを示す。
- **既定**：build未設定時はdimension=`minecraft:overworld`・origin=(200,0,200)。
- **Scratch は y 封印**：標準 UI では `origin.y` を編集可能にしない。ただし Y を完全に隠すのではなく固定値 `0` として見せ、`setBuildOrigin` / wire `build.setOrigin` には y=0 を送る（`2026-07-02-03`）。
- **scope は stream 個別**（`2026-06-24-01`）：build state は接続（stream）ごとに保持。

> 却下＝座標規範を DECISIONS 止まりにし wire doc に書かない：ワイヤ符号化の SSOT が座標意味論を欠くと、plugin/Python が別計算をしても契約上は「合致」に見え、疎通 Layer 2 まで検出されない。符号化（§7④）と規範は別物で、規範は先に固定できる。

### 5.0.1 連続座標・角度の正準数値表現（確定 `2026-08-19-01`）

Minecraftの状態から取得してwireへ返す連続位置は小数第3位、角度は小数第2位へ十進`HALF_UP`で
丸める。`-0`は`0`へ正規化し、JSON numberのまま返す。`1.230`のような末尾ゼロはwireで要求せず、
同じ数値の`1.23`を正準値として扱う。

- 連続位置：`x`／`y`／`z`を小数第3位。例：`1.2345 → 1.235`、`-1.2345 → -1.235`。
- yaw：任意の有限入力を受理する。出力は`[-180,180)`へ正規化して小数第2位へ丸め、丸め結果が
  `180`になった場合は`-180`へ再正規化する。例：`180 → -180`、`181 → -179`、`-181 → 179`、
  `540 → -180`。
- pitch：有限入力`[-90,90]`を両端込みで受理する。範囲外は副作用前に`invalid_params`とし、
  clamp／wrapしない。Minecraftから取得した出力は小数第2位で返す。

入力座標・角度はfinite／値域を検査するが、上記の表示桁へ丸めてから副作用を実行しない。
成功responseは入力値のechoでなく、適用後のMinecraft状態を読み直して本節の正準化を行う。
integerと定義されたblock座標、height、count、sequence等には本節の丸めを適用せず、小数入力を
黙ってintegerへ変換しない。offset、speed、radius等の非座標scalarは各methodの個別contractを正とする。

正準化はpluginが一度だけ所有する。Python／Scratch／WireScopeは受信したwire numberを再丸めせず、
UIが末尾ゼロを補って表示しても保持値とframeを変更しない。eventの連続位置はlistenerでcaptureするときに
正準化してimmutable DTOへ入れ、poll時の再計算やclient別変換を行わない。artifact b4以前のraw出力は
履歴として維持し、本契約はartifact b5のcompatibility setから適用する。

### 5.1 DimensionKeyとbuild setter（protocol 22）

現行の完全な入力／出力、surface投影、protocol 21非互換境界は
[DimensionKey設計](dimension-key-design_ja.md)を説明正本とする（`2026-08-22-02`）。

- `DimensionKey`は完全修飾`namespace:path`。出力は常に完全修飾する。
- 入力`DimensionRef`は完全修飾key、または`minecraft` namespaceだけを省略したpath。省略時だけ`minecraft:`を補う。
- `world`／`normal`／`nether`／`end`をaliasにしない。case変換、trim、Environment／folder名fallbackを行わない。
- pluginは`Bukkit.getWorld(NamespacedKey)`でloaded dimensionを解決し、`World#getKey()`を出力する。
- wireは`build.setDimension [dimension_ref]`と`build.setOrigin [x,y,z]`。両者は成功時にexact
  `{ "dimension": <DimensionKey>, "origin": [x,y,z] }`を返す。
- clientはsetter入力で現在contextを更新せず、hello／成功resultだけを正とする。
- protocol 21／b4以前の`build.setWorld`／`setWorld()`／`world` fieldは履歴として保持するが、protocol 22へ移行しない。

Scratchは標準menuに`overworld`／`the_nether`／`the_end`を提示できるが、wireを3dimensionへ閉じない。
`setOrigin`の標準UIでy=0固定とする既存学習導線は維持する。

---

### 5.2 player.getPos / player.setPos（b2 準核）

`player.*` は paired player を対象にする操作群で、identity は hello/auth が確定した token に束縛された UUID から解決する。クライアントは player 名を送らない。

- **`player.getPos`**：paramsは`[]`。paired playerの現在dimensionと現在位置を返す。resultは
  `{ "dimension": "minecraft:overworld", "pos": [x,y,z] }`。`pos`はstream origin相対で、
  `stream.dimension`とplayerの現在dimensionの一致を要求しない。artifact b5以後は§5.0.1も適用する。
- **`player.setPos`**：paramsは`[dimension_ref,x,y,z]`。serverがDimensionRefを§5.1で解決し、
  `absolute = stream.origin + relative`を計算して指定dimensionへteleportする。成功resultはgetPosと同形。
- **originとの関係**：`player.*`はstream originを共有するが`stream.dimension`へ暗黙依存しない。
  `world.*`は`stream.dimension + stream.origin`、`player.*`は`explicit/current dimension + stream.origin`で読む。
- **権限**：許可/拒否は LuckPerms に委譲し、protocol 独自の teleport 権限体系は作らない。拒否は `permission_denied`。
- **基本reason**：`permission_denied`／`player_offline`／`unknown_dimension`／`invalid_params`。

> 却下＝`player.getPos`を`stream.dimension`不一致時errorにする案：resultに現在dimensionを明示すれば不一致は状態でありエラーではない。却下＝`player.setPos`が暗黙に`stream.dimension`を使う案：dimensionを引数で明示する方が次元跨ぎteleportとorigin相対の関係を説明しやすい。却下＝McRemote独自のteleport権限を新設する案：認可体系をprotocolに増やさずLuckPermsに一本化する。

### 5.3 player.getPose / player.setPose（b4 実装予定）

`player.getPose` / `player.setPose` は §5.2 の `getPos`/`setPos` に**向き（yaw/pitch）を加えた版**で、b4 の実装予定に含める（DECISIONS `2026-07-29-03`）。API 層名は `getPose`/`setPose`、wire method は `player.*`。既存 `getPos`/`setPos` は廃止せず維持する（用途に応じて位置のみ／位置＋向きを使い分ける）。

- **`player.getPose`**：paramsは`[]`。resultは
  `{ "dimension": <DimensionKey>, "pos": [x,y,z], "yaw": ..., "pitch": ... }`。
- **`player.setPose`**：paramsは`[dimension_ref,x,y,z,yaw,pitch]`。§5.2と同じ解決・座標式を使い、
  **位置と向きを1回のteleportで一体反映**する。成功resultは`getPose`と同形。
- **値域と出力正準形**：`x`/`y`/`z`/`yaw`/`pitch` は有限値必須（NaN/Infinity は `invalid_params`）。`yaw` は任意の有限値を受け入れ、resultでは`[-180,180)`へ正規化する。`pitch`は`[-90,90]`を両端込みとし、範囲外は`invalid_params`で副作用前に拒否する。入力を丸めてからteleportせず、成功後に再取得した位置を小数第3位、yaw／pitchを小数第2位へ§5.0.1どおり正準化する。
- **teleport失敗**：teleport自体が失敗した場合（`permission_denied`／`player_offline`／`unknown_dimension`／`invalid_params`のいずれにも当たらない要因でPaper `Entity.teleport(Location)`がfalseを返す等）を成功扱いにせず、`teleport_failed`を返す。
- **範囲**：b4 の対象は paired player までとし、任意 entity への pose 操作は将来拡張とする。
- **高水準 walkThrough（構想・未確定）**：`player.walkThrough` は軌道・速度・補間・注視方向をクライアント側で組み立て、`getPose`/`setPose` を基礎命令として使う構想。正確な API 形と収容版は別途決定する。

> 却下＝旧 `camera.setNormal`/`setFixed`/`setFollow`/`setPos`（RemoteControllerMod のクライアント mod 側カメラ操作）を Paper 側 API として再現する案：対応する汎用 camera API が Paper に無い。却下＝`setSpectatorTarget` を walkthrough の基盤にする案：spectator mode 必須で entity 追従以外の pose を直接指定できない。却下＝位置と角度変更を別 request にする案：途中状態が見え1フレーム内で位置と視線がずれ得る。却下＝walkThrough 全体を server 側の長時間 job として先に固定する案：円弧・Y 補間・look-at 等はクライアント側の高水準処理として組み合わせやすい。

### 5.4 events.poll と有限event ring（protocol 22／b5、protocol 23／b6）

server pushは使わない。pluginはpaired playerに発生した対象eventを、そのplayerへ束縛された全active
connection epochのringへimmutable DTOとして複製する。epochごとにring、sequence、cursorを独立させ、
別sessionのpollでeventを失わせない。sequenceはepoch内で1から単調増加し、disconnect／reconnectで
ringとともに破棄する。reconnect replayは行わない。

`events.poll`は`[after_sequence]`または`[after_sequence,{"max_events":N}]`の非破壊pollである。
`max_events`は正integerのclient希望上限で、省略時はserver既定を使い、指定時はclient値とserver上限の
小さい方を適用する。server上限を超える希望値をerrorにせず、未知option、0、負数、非integerは
`invalid_params`とする。件数上限より先にbyte上限へ達した場合は、収まるeventまでを返す。
response喪失時は同じcursorで再取得でき、clientはresponseを正常受理した後だけ`through_sequence`まで
cursorを進める。filterを採用するreleaseでは同じoptions objectを精密化し、b5 clientへ別のpoll methodを作らない。

- `after_sequence`がretained oldestより古い: lossを伴う有効なpoll。残っている先頭から返す。
- `after_sequence`がlatestと同じ: 空の有効response。
- `after_sequence`がlatestより大きい: `invalid_params`。
- ring overflow: 最古eventから退去させる。沈黙したlossにしない。
- compact JSON-RPC response: 最大61,440 bytes（60 KiB）。WireScopeの64 KiB encoded frame admissionへ
  4,096 bytesの余裕を残す。b5では最大合法responseをobserver schema v1（compatibility revision v1.1）／session envelopeまで投影し、
  UTF-8 encoded frameが65,536 bytes以下となることをescape量の多い文字列を含むfixtureで確認する。

responseは`events`、`through_sequence`、`latest_sequence`、`filtered_out`と、epoch内で単調増加する
`overflow_dropped_total`、`capacity_dropped_total`、`explicitly_discarded_total`を持つ。
`capacity_dropped_total`はresource／capacity admissionによりringへ投入できなかったeventを数える。
b5ではfilterとclearを実装せず、`filtered_out`と`explicitly_discarded_total`は常に0とする。

後続filterはringをsequence順に走査する。非一致eventでも`through_sequence`を進め、
`filtered_out`へ加算するがlossには数えない。`events.clear`は呼出時点までのretained eventを削除し、
`explicitly_discarded_total`へ加算する。

b5のevent typeは次の3種である。exact JSON shapeはplugin fixtureを拘束層とし、Bukkit Event objectを
wireやringへ保持しない。

- `block_right_click`: 発生時のdimension／origin、origin相対block position、face、protocol 22の`BlockValue`、hand。
  相関するmain／off-hand二重発火は1件へ正規化する。
- `chat_posted`: paired playerが投稿したoriginal plain input。slash commandは除外し、chat自体はcancelしない。
- `projectile_hit`: 発生時のdimension／origin、projectile type、hit position、blockまたはentity target。block targetはprotocol 22の`BlockValue`を持つ。
  player hitは`kind: "player"`だけとし、handle、UUID、player nameを返さない。

`block_right_click`のblock positionはintegerのままとする。`projectile_hit`の連続hit positionは発生時の
captureで§5.0.1の小数第3位へ正準化し、後から丸め直さない。

**protocol 23／b6の置換（確定 `2026-08-26-06`）**：b5で配布済みの`block_right_click`はprotocol 22の
`released` eventとして履歴と互換契約に残し、b5 artifactを差し替えない。有限ringを通常playの右click noiseが
消費する不備を直すため、protocol 23では`block_right_click`を削除し、次の`pickaxe_poke`へ置き換える。

- type: `pickaxe_poke`
- gate: `org.bukkit.Tag.ITEMS_PICKAXES`に合致する所持itemでのblock右click
- payload: 旧eventの`pos`／`face`／`block`／`hand`に、item type keyのcanonical文字列`item`を追加
- delivery: `sessionsFor(event.getPlayer())`。player identityはpayloadへ追加しない
- interaction: `ignoreCancelled=true`の観察専用。対象blockのvanilla interactionをcancelしない
- cardinality: 同一player／dimension／x／y／z／tickの2回目callbackはhandに関係なく重複として1件へ正規化する

同名eventをpickaxe限定へ狭める案、旧新eventの恒久二重配送、bN／capability判別の新設は採らない。

McRemote `codex/b6-pickaxe-poke@b0f5503301f9ca1b8226eea0c6ca56c947aab196`は本contractと
protocol `23.0.0`／artifact `2300.0.0b6`への移行をplugin実装済みである（`2026-08-26-07`）。
unit／deterministicと対象live-humanの実施報告がある。scratch-editor
`agent/b6-pickaxe-poke@e6b0d35cd2`はclient側のprotocol `23.0.0`、`PickaxePokeEvent`、
`events-v23.json`、Scratch hat／event context、WireScope observer投影を実装し、対象test／lint／buildを
PASSしたpush済みcandidateである。pluginとの実接続によるlive-human、正式evidence record、default branch
統合、exact横断candidate、artifact統合／releaseは別gateであり、局所実装から完了を推測しない。

空間eventは投入時点のdimensionとoriginを固定する。後からbuild dimension／originが変わっても既存DTOを変更・
破棄せず、event受信を理由にpluginがbuild stateを暗黙変更しない。event座標を`world.*`へ渡すclientは、
現在のdimension／originとの一致を確認し、不一致をactionable errorとして扱う。

### 5.5 connection epoch scoped entity handle（b5）

protocol 22／b5のentity handleは`mceh_`、protocol 23／b6以降に新規発行するhandleは`mcr_eh_` prefixと
128 bit以上の暗号学的乱数に由来するopaque ASCII stringである。prefix以外の意味論は同じとし、protocol 23で
`mceh_`をalias受理しない。disconnectで全handleが失効するためmigrationは作らない。
UUID、dimension、player、credentialを符号化せず、秘密や認可capabilityとして扱わない。同一epoch内では
同じentityに同じhandleを返し、disconnect／reconnectで全て失効する。WireScope表示やScratch変数への
格納は許可するが、操作のたびにepoch ownershipとpermissionを再検証する。

- foreign／unknown handleはどちらも`entity_handle_not_found`へ畳む。
- playerにはhandleを発行せず、player操作は`player.*`に限定する。
- spawn前にhandle slotを予約し、予約不能ならdimensionを変更せず`entity_capacity_exhausted`。
- 外部要因でentityがdimensionを移動した場合は失効する。成功した`entity.setPose`による移動ではissued dimensionを更新する。
- known handleの対象状態は`entity_removed`、`entity_unloaded`、`entity_dimension_changed`で区別する。
- spawn自体の失敗は`entity_spawn_failed`。spawn後にresponseを喪失した場合は結果不明であり、自動retryしない。

### 5.6 world.getHeight（b5）

paramsは`[x,z]`または`[x,z,max_y]`、resultはinteger。`x`、`z`、`max_y`、resultはstream origin相対で、
`max_y`はinclusiveである。省略時は`world.maxHeight - 1 - origin.y`を使う。

指定列を上から探索し、非passable blockかつ直上がpassableとなる最上面blockの相対yを返す。
world上端の直上はpassableとして扱い、該当が無ければ`height_not_found`。走査量はavailability guardへ
計上する。独立した`world.findFloor`は作らず、低い`max_y`を指定した反復で多層を探索できるようにする。

### 5.7 world.spawnParticle／world.spawnEntity（b5）

`world.spawnParticle`は座標先行の9個または10個のpositional params
`[x,y,z,offset_x,offset_y,offset_z,particle,speed,count,(force)]`を受ける。`force`は省略でき、
省略時は`true`とする。`x`／`y`／`z`はstream origin相対の連続座標で、副作用前に表示桁へ丸めない。
offset三軸とspeedは有限の非負number、countは非負integer、指定したforceはbooleanでなければならない。
particleにはcatalogのcanonical namespace IDを使う。b5はdata不要particleだけを受け、未知IDは
`unknown_particle`、typed data必須は`particle_data_required`。count、offset、speed、work量を副作用前に
検証し、resultには実際に受理したparticle countを返す。

`world.spawnEntity`はexact 4個のpositional params `[x,y,z,entity]`を受ける。`x`／`y`／`z`はstream
origin相対の連続座標で、副作用前に表示桁へ丸めない。entityにはcatalogのcanonical namespace IDを使い、
成功時は§5.5のhandleを返す。playerまたはspawn不能typeは`entity_not_spawnable`、未知IDは
`unknown_entity`。handle capacity、permission、chunk／work admissionをspawn前に検証し、未知IDを
`minecraft:cow`等の別entityへfallbackしない。

protocol 22ではparticle-first／entity-first順序とのunion受付や、型による旧新順序の自動判定を行わない
（DECISIONS `2026-08-21-01`）。

availability reasonは追加の`retryable` fieldを作らず、次の意味を固定する。

- `backpressure`: 副作用開始前。後で同一要求をretry可能。
- `work_limit_exceeded`: 入力量を減らす必要があり、自動retry禁止。
- `entity_capacity_exhausted`: 自動retry禁止。
- `permission_denied`: permission変更までretryしない。
- `internal_error`: 結果不明。非冪等操作を自動retryしない。

### 5.8 b6 signとb7 direction／b8 entity lifecycle

b7 directionは`player.getDirection`／`setDirection`／`entity.getDirection`／`setDirection`を一組にする。
getは向きを正規化した単位vector、setは有限な非zero vectorの大きさを捨てて向きだけへ正規化し、位置と
dimensionを変更せず適用する。zero vector error、exact params／result、出力精度はb7 contract lockまで
推測しない。rotation／pitch／yawを個別にget／setする六methodは採らない。

b8 entity lifecycleはprotocol 22で固定したpose shape `{dimension,pos,yaw,pitch}`と§5.0.1の出力正準形を
protocol 23へcarryする。nearby検索はstream dimension内、player除外、radius／件数／chunk走査をboundedにし、
unloaded entityを探すためのchunk loadを行わない。必要なhandle capacityはrequest全体で事前確認し、部分的な
handle発行をしない。一覧は`handle`／canonical `type`／`pos`を持つsnapshot方向とし、direction／full poseは
個別getterに任せる。`entity.remove`成功時はhandleを即時失効する。exact params／result shapeはb8 contractを
実装前に固定する。

sign APIは`world.getSign`、`world.setSign`、`world.updateSignLine`をb6へ配置する。三層モデルのread／replace／
最小PATCHを比較する一組だが、GET＋PUTによるclient／ユーザーコードの合成も有効な学習経路として残す
（DECISIONS `2026-08-26-03`〜`05`）。exact contractは§5.8.1を正とする。

typed particle dataは条件付きb9以降のcandidateとする。採用時もdustとblock stateの有限schemaだけを扱い、
任意Java objectの直列化とitem particleを同じsliceへ入れない。

#### 5.8.1 sign exact contract

signの入力値と正準出力値を次で固定する。

```text
LineSpec  = string | {text:string, color?:string, decorations?:string[]}
LineValue = {text:string, color:string, decorations:string[]}
```

裸の`string`はplain textのshorthandである。`color`はAdventure `NamedTextColor`標準16 token、すなわち
`black`、`dark_blue`、`dark_green`、`dark_aqua`、`dark_red`、`dark_purple`、`gold`、`gray`、`dark_gray`、
`blue`、`green`、`aqua`、`red`、`light_purple`、`yellow`、`white`、または`#RRGGBB`を受理する。
`decorations`は`bold`、`italic`、`underlined`、`strikethrough`、`obfuscated`だけを受理する。任意JSON Component、
click event等、それ以外のstyleは受理しない。

`LineValue`は全fieldを常に出す。無色は`color:"black"`へ正規化し、`decorations`はtoken名の昇順、すなわち
`bold`、`italic`、`obfuscated`、`strikethrough`、`underlined`の順で出力する。

| method | params | result | 更新単位 |
| --- | --- | --- | --- |
| `world.getSign` | `[x,y,z]` | `{front:[LineValue×4],back:[LineValue×4],waxed:bool}` | 読取りのみ。waxedでも許可 |
| `world.setSign` | `[x,y,z,{front?:[LineSpec×4],back?:[LineSpec×4]}]` | `null` | 指定した各面を厳密4行で置換。面内no-merge |
| `world.updateSignLine` | `[x,y,z,face,line_index,LineSpec]` | `null` | `face="front"|"back"`の一行だけ。`line_index`は0始まりの`0..3` |

`world.updateSignLine`は指定した一行以外の同じ面の3行と反対面を保持する。入力型、shape、face、index違反は
`invalid_params`とし、安全に原因位置を特定できる場合は`data.path`を付ける。文字列だが許可外の色または装飾tokenは
`invalid_property_value`とし、`data.property`を`"color"`または`"decorations"`、併せて`data.value`と
`data.allowed`を返す。

readのreasonは`invalid_params`／`not_a_sign`だけとし、waxedでも読み取れる。writeのreasonは
`invalid_params`／`not_a_sign`／`sign_waxed`／`invalid_property_value`／`sign_update_failed`／
`permission_denied`／`build_denied`／`backpressure`／`work_limit_exceeded`とする。

writeは全入力とavailabilityを検証してから、sign state全体に対する一つのmutationだけを行う。stale snapshotなら
書込み前に拒否し、部分変更を残さず`sign_update_failed`を返す。「書いてから元へ戻す」rollbackをcontractにしない。
現McRemote candidateはPaper `BlockState.update(force=false, applyPhysics=false)`の拒否でこの保証を実装する。

McRemote `codex/b6-set-sign@a34fec0b64a5c939687de4a89fb94e2728d2e116`はpush済みplugin candidateで、129 unit tests、
Paper 1.21.11 live-auto、5装飾と一行限定更新のlive-human PASSが報告済みである。ただしstale snapshot競合を
意図的に再現したlive検証と、`updateSignLine`の`sign_waxed` live-humanは未実施。Python
`codex/b6-protocol23-python@69a160aecfc6cd346b3341cdf10007e2903b5207`とScratch
`agent/b6-pickaxe-poke@9dbdc1aeb00e9873cf0eb4de226c11acb4ea0cb4`にもpush済みclient candidateがある。
Scratchはreadでfull `LineValue`を保持し、writeでは`LineSpec`のstring shorthandだけを公開する。このsurface
絞り込みはobject形式のwire受理を狭めず、Scratchから色／装飾を書けるとは主張しない。共有横断fixture、
実pluginとScratchのsign live、artifact統合、releaseは未完であり、局所実装からこれらを推測しない。

---

## 6. helloペイロード

protocol 23の現行helloはprotocol 22で確定したJSON-RPC／auth／catalog／world constants／DimensionKeyの骨格を
そのままcarryし、`protocol`だけを`23.0.0`へ上げる。build要求は`dimension`／`origin`、応答は完全修飾
`dimension`を返す。protocol 21の`world` fieldとprotocol 22の版値は履歴でありunion受理しない。

### 6.1 要求 `params`（object）

```json
{ "protocol": "23.0.0", "client": { "name": "...", "version": "...", "locale": "..." },
  "auth": { "token": "..." }, "build": { "dimension": "minecraft:overworld", "origin": [200, 0, 200] } }
```

- `protocol` ＝protocol semver `23.0.0`。package版`2300.0.0b6`を載せない。protocol 22／b5以前の版値は履歴である。
- `sandbox` は **`hello.params` に載せない**。bridge 経由の Sandbox routing は §2 の WSS 接続メタ（例 `?sandbox=...`）が担う。直 TCP 経路では接続先 host/port が routing 情報であり、plugin が受け取る wire payload は bridge 経由でも直 TCP でも同一に保つ。
- `auth` は **`{ token }` の1モード**（token はサーバで player 束縛）。**ペアリング（token の入手）は hello の前段の独立メソッド `auth.pairBegin` / `auth.pairPoll`**（§6.5・確定 `2026-07-04-06`）＝hello 自体は pair モードを持たない。`build`省略時はdimension=`minecraft:overworld`・原点(200,0,200)。`build.dimension`は§5.1のDimensionRefで、成功resultは正準DimensionKeyを返す。
- **enforcement トグル連動**（plugin config・§10.11.1 項5）：hello の `auth` 扱いはトグルで変わる。**OFF（開発既定）**＝`auth.token` 欠落/空を許容し**無認証セッション可**（3リポ非同期着地のため・item5）＝この段では最小必須は `{ protocol }`。**ON（リリース既定）**＝`auth` 必須で、欠落→`auth_required`、検証失敗→`token_expired` / `token_revoked` / `token_not_found` / `token_invalid` 等の認証 reason（§6.3）。構文不正・未知形式・検証不能は `token_invalid`。

### 6.2 応答 `result`

```json
{
  "protocol": "23.0.0",
  "mc_version": "1.21.11",
  "supported_mc_versions": ["1.21.11"],
  "catalogHash": null,
  "world_constants": { "y_sea": 62 },
  "session": "...",
  "player": "...",
  "dimension": "minecraft:overworld",
  "origin": [200, 0, 200],
  "permissions": { "online": true, "offline": false, "buildRange": 100 },
  "server": "..."
}
```

- **protocol 23安定形**：protocol 22のhello shapeを変更せずcarryし、版値だけ`23.0.0`へ上げる。応答は`{protocol,mc_version,supported_mc_versions,catalogHash}`にsession／player／`dimension`／origin／permissionsを加える。`dimension`はserverが解決した完全修飾DimensionKeyで、clientは要求値で上書きしない。world/profile情報定数は`world_constants` bucketへ束ねる。`catalogHash`と`world_constants`の既存規律は維持する。
- **§8 整合**：versioning-design §8.1 が要求する `mc_version` / `supported_mc_versions`（踊り場リスト）を応答に含める（§8.1 必須ゆえ省けない）。互換判定は §8 のメジャー一致則に従う。
- **`permissions.buildRange` の意味論**（確定 `2026-08-06-01`）：hello が返す整数値と server の実際の build guard は、paired UUID に対する同じ `PermissionProvider` の値解決経路を使う。LuckPerms 使用時は、既存 `QueryOptions` における User の effective meta を正本とし、McRemote が primary group だけを直接読んだり、user node・継承・context・weight・meta stacking の優先順位を再実装したりしない。meta key、context、meta 欠落または整数 parse 失敗時の `0`、LuckPerms 不在時の fallback は既存どおり。これは既存 field の値解決修正であり、wire field 名・shape・protocol `21.0.0` を変更しない。負値の意味論は別判断とする。
- **`catalogHash`**（確定 `2026-06-26-03`・§7.2）：ブロック等カタログのキャッシュ識別子＝`mc_version`/`supported_mc_versions` 広告に**紐づくレジストリ指紋**（重複フィールドにしない）。クライアントは `catalogHash` が実値で、その hash に一致する cache を持たない場合にだけ本体を取得する。`catalogHash` が null なら本体を取得しない（b1 は無認証ゆえ常に null）。**クライアント別の非同梱・利用規則は §7.2 に従う**（`2026-08-02-05` / `2026-08-02-07` で「同梱既定版 fallback」は Python・Scratch とも廃止済み）。
- **`world_constants`**（確定 `2026-07-02-02`）：world/profile 依存の情報定数を束ねる object。b1 では object と `y_sea` key の存在だけを確認対象にする。wire key は `y_sea`、値は `number | null`。Python 生成定数名として `Y_SEA` を使うのは可。`y_sea` は座標式には使わず、完全な意味論、superflat 判定、full `world_constants.json` 配送、multi-version switching は bN / domain knowledge 側へ送る。**値は `world.getSeaLevel() - 1`（最上段の水ブロックの標高）**とする（`2026-07-30-01`）。`getSeaLevel()` 自体は `00-hub/world-constants-facts_ja.md` の `y_ground`（水面直上・地表の配置基準）に当たり、`y_sea` とは1ブロック異なる。

### 6.3 失敗

認証系（token 破棄＋再ペア）＝`token_expired` / `token_revoked` / `token_not_found` / `token_invalid` / `auth_required`（enforcement ON で token 欠落）。認可系（token 温存・操作のみ拒否）＝`permission_denied`。版不一致は認証系に混ぜず §8 `protocol_mismatch` に隔離。ペアリング固有の reason は §6.5。エラー形は §3.3 の JSON-RPC error オブジェクトに載せ、意味は §7.3 の二層（`code`＝`-32000`番台／`data.reason`＝小文字スネーク enum）で運ぶ。

### 6.4 確定済みの決定事項（auth 以外）

pair→tokenの入手フロー（§6.5）／origin基準の相対座標／`protocol`で版交渉／権限を応答でsurface／最小必須`{protocol}`（enforcement OFF）または`{protocol,auth:{token}}`（enforcement ON）・build省略時dimension=`minecraft:overworld`／origin=(200,0,200)。authフローは§6.5、DimensionKeyは§5.1に従う。Sandbox routingはhello payloadではなく§2のbridge routingが担う。

### 6.5 認証：ペアリングフロー（確定 `2026-07-04-06`）

token の入手＝ペアリング。**hello の前段の独立メソッド `auth.*`**（hello は §6.1 の `auth:{token}` 1モードのみ）。トポロジは **poll**。`auth.pairPoll`をserver→client notificationへ差し替えず、server pushを採らない`2026-08-16-05`の規律を適用する。名前空間 `auth.*` は将来の `auth.refresh` / `auth.revoke` / `auth.logout` も同居させる。**`auth.listCredentials` / `auth.revoke` / `auth.logout` は `2026-08-02-01` で確定し §6.6 に置く**（`auth.refresh` は自動期限を設けないため予約のまま）。

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

- **`auth.pairBegin`** `params`＝`token_type`（`"session"`\|`"long_lived"`・既定 `"session"`。**`2026-08-02-01` で `"player"` から改名**＝`"player"` は新規発行で受理せず、未知値は `session` へ黙って丸めずに `invalid_params` を返す）／`client`（`{name,version,locale}`）／`device?`（long-lived credential のデバイス別発行・`last_used_at` と併せた表示用ラベル。trim 後 1〜64 文字・重複可・**認証要素ではない**）。**`protocol` は載せない**（版交渉は hello の責務・identity は版非依存で不一致は hello が弾く）。`result`＝`{ pairing_id, pair_code, expires_in }`（`pair_code`＝6桁数字・約120秒・1回限り）。
- **pair code 表示**（DECISIONS `2026-07-07-01`）：wire の `pair_code` は素6桁 ASCII のまま不変。人間向け UI は `NNN-NNN`（例 `333-333`）で表示し、コピー対象はコマンド全体 `/mcremote pair NNN-NNN` を既定にする。plugin の `/mcremote pair` 入力は区切りとして入り得る非数字（`-`・空白等）を除去し、残りが ASCII 数字 `0-9` の6桁である場合だけ bind する（全角数字は変換しない）。これは表示・人間入力の規約であり、`auth.pairPoll` は引き続き `pairing_id` 相関で wire に `pair_code` を戻さない。
- **相関の分離**：`pair_code` は人間が`/mcremote pair <code>`で使う約120秒・一回限りの表示・操作用コードであり、credentialや永続的な秘密ではない。通常log、transcript、公開evidenceへ収録でき、必須redaction対象にしない。`pairing_id`はtokenを受け取る`auth.pairPoll`のwire相関子であり、pair codeとは異なり公開logへ出さない。plugin が `pair_code → pending(pairing_id)` を保持し、`/mcremote pair` 実行者の UUID を pending に束縛する（正本＝plugin・bridge は透明中継）。
- **`auth.pairPoll`** `params`＝`{ pairing_id }`。`result`＝`{ status:"pending" }` または **`{ status:"ok", token }`（最小）**。**`pending` は error でなく `result.status`**（待機は失敗でない）。失敗は error＝`pair_expired`（code TTL 経過）／`pair_not_found`（不正な `pairing_id`）。token は**要求した1種のみ**発行（`session_token`/`long-lived credential` を同時発行しない）。
- **単一ソース原則**：`pairPoll` の `ok` は **token だけ**返す。`player`(UUID)・`permissions`・`world`・`origin` は**続く hello の `result` が単一ソース**（§6.2）＝pairPoll に冗長フィールドを持たせない。`token_type` も prefix（`mcrs_`/`mcrl_`）と要求から自明ゆえ返さない。WireScope（#13）は権限・world を hello から読む。
- **bridge 透明性**：poll は `pairing_id` で相関するため、`pairBegin`↔`pairPoll` で同一 TCP 接続を保持する必要がない（sticky TCP 不要）。ただし Sandbox route は WSS 接続メタとして bridge 側が保持する（§2）。plugin 側 TCP が `auth_required` / 認証系 reason の後で閉じても、同一 browser-side session の `auth.*` と再 `hello` は同じ Sandbox へ送る。`2026-08-17-01`により、Scratch–Bridge transportは`auth.pairBegin`／`auth.pairPoll`だけにJSON-RPC外のone-shot hintを使える。Bridgeが解釈するのはhintだけで、raw JSON-RPC payloadを解析・変更しない。hintはplugin TCPへ送られず、plugin wire、method、params、response、protocol `21.0.0`を変更しない。固定delay、EOF待ち、自動再送をplugin wireの規律として導出しない。
- **token 種別**（`2026-08-02-01` で改名・旧記述は scratch-plan §2.5）：`session_token`（`mcrs_`・約2h・Scratch/一時利用。**`2026-08-02-08` で hash-only record として永続化**＝通常の plugin / server 再起動を跨いで `expires_at` まで再利用でき、socket / stream / build state は再起動で失われて再接続時に新規生成する。§6.6 の管理 wire の対象にはしない）／**`long-lived credential`（`mcrl_`・`token_type: "long_lived"`・サーバ再起動を越えて有効・明示 revoke まで有効・`expires_at = null`・デバイス別・CLI `login`）**。旧称 `player_token` / `mcrp_` は使わない（`player_token` は「player に属する」意味に読めるが session token も player UUID に束縛されるため区別にならない。実際の区別は寿命と失効経路）。**移行**＝新実装は `mcrp_` を新規発行せず、保存済み `mcrp_` は `token_not_found` 等の既存認証 reason で無効化する。client は破棄して一度だけ `mcrl_` を再取得する（`2026-07-04-03` 項3 の破棄側フローに乗る）。**一時的な二重 prefix 発行期間は設けず**、plugin / Python / Scratch の wire 変更は同一互換単位で着地させる。改名を credential 実装から切り離して先行させない（理由と全規則は `11-plugin/platform-design_ja.md` §9.8）。Scratch の標準導線は session のみ。**Python の既定 credential を long-lived へ切り替える公開導線は開いていない**＝gate は versioning-design §10.11.2 が正本で、開放条件は `2026-08-02-03` に置く。サーバは生 token を保存せず SHA-256 hash のみを持ち、認可は常に UUID→LuckPerms。
- **credential scope**：tokenはopaqueなままとし、channel / Sandbox名をwire tokenへencodeしない。serverごとのcredential storeが未知tokenを拒否し、client storeはcredentialを接続先profile / targetへ紐づけて別channel・別Sandboxへ黙って送らない。将来複数serverがcredential storeを共有する場合だけ、明示的なaudience / scopeをprotocol ratifyする。
- **PoPは未批准**：公開鍵付きpairing、challenge / nonce、proof、signature errorは現protocolへ追加しない。接続時Proof of Possessionはtoken文字列だけの別端末再利用を抑えるhardening候補だが、b4 / rc / public betaのgateから外した（DECISIONS `2026-07-16-03`）。採用判断までalgorithm、key encoding、canonical bytes、challenge wire shapeを推測で固定しない。Bridgeは採用後もpayload-transparentであるべきだが、これは現時点のwire契約追加ではない。
- **クライアント契約（reason 駆動・OFF/ON 統一）**：クライアントは**まず `hello`（token を持てば載せる）を試み、`auth_required` が返ったときだけ**本フロー（`pairBegin`→`pairPoll`→再 `hello`）に入る。この1経路が OFF/ON/token 失効を統一する＝**enforcement OFF（開発既定）では token 無し hello が成功し `auth_required` が返らない＝ペアリングは自動的にスキップ**（dev 動線に別コードパス不要・§6.1・item5）。ON では token 欠落時に `auth_required`、token 検証失敗時に §6.3 の認証系 reason が返る。認証系 reason で token を破棄したら同じく先頭（hello 試行）へ戻る。
- **非規範（クライアント実装の目安・ratify 対象外）**：poll 間隔 ≈1–2s、poll の timeout は `pairBegin` が返す `expires_in`（`pair_code` TTL・≈120s）で、超過は `pair_expired` として扱う。`pairing_id` はクライアント in-memory 保持でよい（リロードで破棄＝ユーザーは接続ブロックを再実行）。

### 6.6 credential 管理（確定 `2026-08-02-01`）

long-lived credential の一覧と失効。認証後のみ有効で、常に**認証中の player UUID に属する credential だけ**を対象にする。method 名は §6.5 が予約していた `auth.*` 名前空間に一致させる（`auth.revokeCredential` のような別名は使わない）。

- **`auth.listCredentials`** `params`＝`[]`。`result`＝`{ credentials: [{ credential_id, type, device, issued_at, last_used_at, expires_at, current }] }`。raw token・token hash・他 player の情報は返さない。`current` は要求元がいま使っている credential を指す＝`pairPoll` が token だけを返す（§6.5 単一ソース原則）ため、**client が自分の `credential_id` を知る唯一の経路**。revoke 済みは返さない。
- **`auth.revoke`** `params`＝`[credential_id]`。`result`＝`{ credential_id, revoked: true }`。同一 UUID の credential だけを対象にし、他 player の ID と存在しない ID は**同じ `credential_not_found`** を返す（存在の隠蔽）。同一 UUID の revoke 済み record への再要求は idempotent success。**success response は対象 credential の durable な失効完了を意味する**。応答後、その credential で認証された **全ての active session** を終了して socket を閉じる（同一 UUID は最大 16 の並行セッションを持てる＝`2026-07-04-03` 項7。一つでも残すと revoke 済み credential が既存接続を通じて動き続ける）。
- **`auth.logout`** `params`＝`[]`。`result`＝`{ credential_id, revoked: true }`（`auth.revoke` と同形。client は `listCredentials` を呼ばずに自分の `credential_id` を知れる）。現在の credential を revoke し、成功応答後に**その credential の全 active session**を終了する。client は成功後にローカル credential を削除する。
  - **適用範囲＝long-lived credential 限定**。session token は `2026-08-02-08` により永続 snapshot record を持つが、**revoke を持たない**（無効化は `expires_at` と credential domain reset だけ）ため、`auth.listCredentials` / `auth.revoke` / `auth.logout` の対象にしない。**session の明示終了は接続の切断として扱う**。
  - **idempotency と応答喪失時の収束**：応答が失われて client が再試行すると、その要求は revoke 済み token を提示するので `token_revoked` になる。**client はこれを logout 成功として扱う**（`2026-07-04-03` 項3 の破棄側なので、token を捨てて再ペアリングへ戻る挙動は logout の意図と一致する）。エラーとして表示しない。
- **上限**：UUID ごとの active long-lived credential 数に設定可能な上限を持つ（初期既定 16）。到達時に古い credential を自動失効させず `credential_limit_reached` を返し、ユーザーが list / revoke する。**`2026-07-04-03` 項7 の並行セッション上限 16 とは別の制約**（同じ数字だが別概念）。
- **実装契約は wire ではない**：永続 backend の分離（`CredentialStore` snapshot と `RevocationAuthority`）、revoke の線形化点、domain 整合、create-only tombstone、fail-close の条件は plugin architecture 側（`11-plugin/platform-design_ja.md`）が正本。wire 上は観測可能な意味だけを定義する＝`credential_store_unavailable` の意味（§7.3）と、success response が durable な失効完了を指すこと。

---

## 7. 未確定（要決定）

| # | 論点 | 状態 |
| --- | --- | --- |
| ① | **block id／state表現** | **改訂確定** `2026-08-19-02`（protocol 22の構造化block value・§7.1） |
| ② | **`world.getBlock` 戻り型** | **改訂確定** `2026-08-19-02`（`BlockValue` object・§7.1） |
| ③ | **notification のエラー方針** | **b1 スコープ確定** `2026-07-01-08`（`2026-06-27-04` / `2026-07-01-06` を改訂）。b1 の setBlock/setBlocks/chat.post は **id 付き同期 request** として扱い、疎通確認・error 観測を優先する。server push方向は`2026-08-16-05`で撤回し、eventは非破壊`events.poll`、command errorは対応requestで観察する。send-only UXは別の体験設計 |
| ④ | **命名系統** | **protocol 22改訂確定** `2026-08-22-02`。wire methodはドット名前空間、build setterは`build.setDimension`／`build.setOrigin`。API名はcamelCase。protocol 21の`build.setWorld`は履歴のみ |
| ⑤ | **権限既定値** | 未決（**plugin/LuckPerms の現実依存**）。hello 応答 `permissions` の既定は config.yml の権限名（`mcr.online`/`mcr.offline`/`mcr.build.range`、scratch-plan §2.5）と実 LuckPerms 既定に律速＝plugin b1/認証 bN で実値を確認して確定 |

> §8 のエラーコード（`PROTOCOL_MISMATCH` 等）と認証系コード（`TOKEN_EXPIRED` 等、scratch-plan §2.5）を JSON-RPC error オブジェクトへどう写像するかの対応表も、ここで確定する。

### 7.1 構造化block value（protocol 22、確定 `2026-08-19-02`）

protocol 22.0.0では、protocol 21の`block_state_ref`文字列を`block_id`と`state`へ分離する。
人間向けの理由、Python／Scratch投影、fixture境界は
[ブロック値・状態・多言語投影設計](block-value-design_ja.md)を正とする。

set入力の`BlockSpec`とget出力の`BlockValue`は同じcontainer shapeを持つ。

```json
{
  "block_id": "minecraft:oak_log",
  "state": {
    "axis": "z"
  }
}
```

- `block_id`はstring必須。入力は`:`無しのvanilla短縮IDを許容し、pluginが`minecraft:`を補完する。出力は常に完全修飾する。
- `state`はobject必須。valueはJSON native scalar（boolean／number／string）とし、array／object／`null`を許容しない。
- 最上位fieldは`block_id`と`state`のexact 2 fieldとし、欠落field／未知fieldは`invalid_params`とする。
- state propertyを持たないblockは`state: {}`とする。field欠落、`null`、空文字を使わない。
- set入力のstateは部分指定を許容し、空objectを含む未指定propertyはMinecraftの既定値で補う。既存block stateとのmergeはしない。
- get出力のstateはfull stateとする。JSON objectのmember順序に意味はなく、consumerは順序へ依存しない。
- deterministic fixture／Scratch内部tokenでは、最上位を`block_id`→`state`、state propertyを名前の昇順でcompact JSON化する。
- `world.setBlock` paramsは`[x,y,z,blockSpec]`、`world.setBlocks`は`[x1,y1,z1,x2,y2,z2,blockSpec]`。
- `world.getBlock` resultは`BlockValue`一つであり、IDとstateを別method／別responseにしない。
- id付き`world.setBlock`／`world.setBlocks`の成功resultは`null`とする。idなしnotificationは成功responseも
  error responseも返さない。set後の状態を観察する場合は`world.getBlock`／`world.getBlocks`を明示的に使う。
- `state:{}`は`BlockSpec`／`BlockValue`内の型不変条件であり、値を返さないset成功の`result:null`を禁止する
  protocol全体の規則ではない。
- event DTO内のblockも同じ`BlockValue`を使い、別のcanonical block stringを作らない。

入力は寛容、出力は正準という`2026-06-27-02`の原則は、文字列文法でなくobject fieldへ引き継ぐ。
protocol 21の文字列`block_state_ref`、`getBlock`文字列result、文字列等価round-tripはb4までの契約として
履歴に残し、protocol 22で互換unionや自動判別を設けない。

### 7.1.1 world.getBlocks（protocol 22、確定 `2026-08-19-03`）

- paramsは6個のorigin相対integer座標`[x1,y1,z1,x2,y2,z2]`。
- 各軸の端点をmin／maxへ正規化し、両端を含める。入力方向でresult順序を変えない。
- x外側、y中間、z内側の昇順で走査し、zを最速とする。
- resultは走査順の`BlockValue` JSON array。座標は各要素へ重複収録しない。
- 各軸のinclusive長は10以下、全体は最大1000件。一軸でも超過すればworld走査前に
  `work_limit_exceeded`を返す。
- params shape／integer違反は`invalid_params`。小数を丸めない。
- `world.getBlockWithData`は`world.getBlock`に包含されるためprotocol 22 registryへ載せず、
  `method_not_found`とする。

### 7.2 カタログ配送・キャッシュ（確定 `2026-06-26-03`）

§7①の単一ソース（versioning-design `2026-06-15-04`）の具体化。状態＝**確定**。

- **単一ソース**＝サーバ稼働中レジストリ（ロード済み mod 含む）から block/entity/particle を生成。Python 定数／Scratch プルダウン／実配置先を一致させる。
- **配送＝認証後**：hello 応答が `catalogHash` を返し、クライアントは**未キャッシュ時のみ**本体取得。
- **キャッシュキー＝`catalogHash`**（版＋mod レジストリ指紋）。
- **ローカル（Python）＝PC グローバルキャッシュ**（`2026-08-06-04`）。root は **`$MCREMOTE_CACHE_DIR` が設定されていればその値、未設定なら `$XDG_CACHE_HOME/mcremote`、`XDG_CACHE_HOME` も未設定なら `~/.cache/mcremote`** とする（言語/プロジェクト横断共有）。project-root の定数ファイルはその生成物。**モジュールは projection を同梱しない**（`2026-08-02-05` で「既定版のみ同梱」から改訂＝catalog が稼働中サーバー由来になり、同梱版が実サーバーを代表しなくなったため。補完が効かない状態そのものを接続への入口にする教材設計）。全版 pack はそれ以前に取りやめ済みで、catalog は接続時にグローバルキャッシュへ充填する。
- **クラウド（Scratch）＝IndexedDB**（オリジン単位・catalogHash キー）。**同梱既定版フォールバックは `2026-08-02-07` で廃止**（旧記述＝「＋同梱既定版フォールバック（FS 不可のため）」）。cache は**オフライン用 catalog ではなく、接続後の再取得を省くための保存**であり、**hello の `catalogHash` と一致した後だけ picker で利用する**。接続前や切断後は cache が存在しても現在の接続先との適合を推定しない。結果として「適合が未確認の catalog を使う」状態が構造的に生じない。
- **§8 整合**：hello のカタログ版識別子は §8.1 がサーバに要求する `mc_version`/`supported_mc_versions` 広告と**一名一義に統合**（重複フィールドを作らない）。`catalogHash` はそれに紐づくレジストリ指紋（§6.2）。
- 前提：「未接続で任意版オフライン切替」は要件から落とす。

### 7.2.1 catalog.get（b3 実装予定・確定 `2026-07-29-04`）

§7.2 の配送方針を実現する具体 wire 契約。出典＝McRemote Codex dev session 確定搬送票（未確定の昇格、`release-close/2100.0.0b2`）。**枠組みを確定し、実際のファイル生成・実測サイズ・Paper API 確認は Python client / plugin dev 側でプロトタイプしてから最終 rc 前に再確認する**（下記の要検証項目）。

- **method**：`catalog.get`。認証後のみ有効（§7.2「配送＝認証後」）。未認証は他 method 同様 `auth_required`。
- **params**：`[]`。稼働中サーバの現在 registry を返すのみとし、稼働中と異なる対応バージョンを明示指定して取得する「環境スイッチング」（旧 `world_constants_provision.md` §4、`00-hub/world-constants-provision-notes_ja.md` に carry 済み）は**v1（b3）の対象外**とし、需要が具体化した bN で別途設計する。
- **result**：
  ```json
  {
    "catalogHash": "...",
    "block": {
      "minecraft:oak_log": { "states": { "axis": ["x","y","z"] }, "default_state": { "axis": "y" } },
      "minecraft:oak_slab": { "states": { "type": ["bottom","double","top"], "waterlogged": [false,true] }, "default_state": { "type": "bottom", "waterlogged": false } },
      "...": {}
    },
    "entity": { "<namespace:path>": {}, "...": {} },
    "particle": { "<namespace:path>": {}, "...": {} }
  }
  ```
  - block entry の `states`/`default_state` は §7.1 の構造化block valueと対応させる。値はJSON native scalar（boolean／number／string）を使い、protocol 22ではclientが`block_state_ref`文字列へ相互変換しない。
  - **block entry の完全 schema と validator 規則は `2026-08-02-04` で確定**＝`states` は property 名 → 許容値の配列、`default_state` は property 名 → 値で、両者の property 集合は一致。各 `states[property]` は空でない配列、値は JSON scalar、1 property 内は同一 JSON 型、重複値は禁止、`default_state[property]` は許容値に含まれる。未知の追加フィールドは将来拡張のため無視可能。catalog validatorは入力支援を担うが、最終的な`BlockSpec`受理はserverが正本である（§7.1、`2026-08-19-02`）。
  - **state signature は wire へ追加しない**（`2026-08-02-04`）。client が `states` から導出する＝property 名の昇順 × JSON 型 × canonical な許容値集合（型順 boolean → number → string、boolean は `false` → `true`、number は昇順、string は辞書順）。`default_state` は含めない。上の例では `oak_log` と他の `axis` だけを持つ丸太類が同一 signature に束なる。
  - entity/particle の内部 schema は block ほど複雑な state を持たないため、最小限の識別子集合として扱い、詳細は実装時に catalog validator（`20-教材/ai-learning-design_ja.md` §7 が前提とする states schema・許容値照合）と合わせて詰める。
- **hash algorithm**：`catalogHash` は catalog 本体（`block`/`entity`/`particle` の3キー、`catalogHash` フィールド自体は除く）を**再帰的キーソート・区切り文字最小化（コンパクト）で直列化した UTF-8 バイト列の SHA-256 hex digest**とする。内容（mod レジストリ構成含む）が変われば必ず hash も変わることを保証し、§6.2/§7.2 の「版＋mod レジストリ指紋」を満たす。
- **配送形**：v1 は**単一 response**。分割・ページングは導入しない（未実測のサイズ問題を先回りしない・YAGNI）。実装時の実測サイズが問題化したら bN で別途拡張する。
- **world_constants は catalog.get に含めない**：`y_ground`/`y_lava`/`y_cloud`/`steve_min_y`/`steve_max_y` 等の次元×世代表（`00-hub/world-constants-facts_ja.md` に carry 済み）は mod レジストリに非依存の静的 domain fact であり、catalog.get の「稼働中 registry から生成」という単一ソース原則の対象外。稼働中 world/dimension/world_type にどの行が該当するかだけを、既存 hello の `world_constants` bucket（現行 `y_sea` のみ、§6.2）を bN で拡張して伝える。これは既存フィールドの拡張であり封筒の破壊的変更ではない。
- **要検証（plugin dev 側）**：`world_constants_provision.md`（旧世代・`00-hub/world-constants-provision-notes_ja.md` に carry 済み）は「スーパーフラットはサーバー自身で認識できないため、クライアント側からの通知が必要」と記すが、この制約が現行 Paper API（`World` の generator 設定取得等）でも成立するかは未確認。自己判定できるなら client 通知は不要になる可能性があり、hello `world_constants` 拡張の設計に先行して確認する。
- **python client 側の projection（確定 `2026-08-02-05`・cache root は `2026-08-06-04`・上の要検証欄への回答）**：§7.2 の PC グローバルキャッシュへ生 JSON を `catalogHash` キーで保存し、そこから project-local に `mc_constants.py` と projection manifest を生成する。**projection は package へ同梱せず Git 管理もしない**（§7.2 の改訂）。再生成の判定は `catalogHash` 単独ではなく **`catalogHash` / generator version / projection schema version の3値一致**で行う＝catalog が同じでも generator を改善すれば再生成される。生成トリガは hello 成功後で、`catalog.get` の失敗は接続や建築を止めず actionable warning に留める。`.pyi` による state 補完は「実現可能だが Pylance 実測前」として b3 の対象外。詳細は `12-python-client/mc-constants-design_ja.md`。

> 却下＝カテゴリ別に `catalog.getBlocks`/`getEntities`/`getParticles` を分ける案：往復が増えるだけで、3カテゴリを束ねるコストは低い。却下＝チャンク配送を先に設計する案：未実測のサイズ問題を先回りして複雑化する。却下＝`catalogHash` を素の version 文字列にする案：同一 MC バージョンで mod 構成が異なる場合を区別できない。却下＝world_constants の全表を catalog.get へ折り込む案：mod 非依存の静的 domain fact を毎接続で運ぶ理由がなく、既存 hello 拡張の枠組みと二重管理になる。

### 7.3 エラー設計（確定 `2026-06-27-03`、`2026-07-01-08` で改訂、`2026-07-07-02` で b2 player reason を追加、`2026-08-02-01` で credential reason を追加、`2026-08-02-02` で `data.ref` 規則を改訂、`2026-08-26-05`でsign reasonを追加）

§7③ の b1 部分を画定。**JSON-RPC 標準 error オブジェクトに一本化**（独自封筒を作らない＝`2026-06-26-01` の標準枠原則に忠実）。`code` は JSON-RPC 標準に従い、**意味は `data.reason`（安定 enum）が運ぶ二層**。UI/AI/test は `reason` を分岐 key にし family（code）を意識しなくてよい。

- **`message`**＝英語短文（ja は client が `reason` から投影）。
- **protocol 21の`data.ref`**＝文字列ref検証で問題入力をエコーした履歴field。protocol 22の構造化block valueでは使用せず、対応する`block_id`／`property`／`value`／`allowed`を返す。state／service／permission等、対応する入力値が存在しないreasonでは意味のないsentinel、空文字、`null`を捏造しない。
- **`data.path`**＝原因fieldを一意に特定できる`invalid_params`で任意。rootは`params`、array indexは
  `[n]`、object fieldは`.name`で連結する（例`params[3].state.axis`）。原因が一つに定まらない場合は
  省略し、入力全体の文字列化を代用品にしない。
- **`data.allowed`**＝`invalid_property_value` で許容値を返せれば返す（**b1 任意 / b2 必須**）。blockはcatalog、
  signは§5.8.1の色allowlist＋hex patternまたは装飾allowlistを正とする。signでは`2026-08-27-03`により
  配列順もcanonicalである。色はMinecraft／Adventureの慣用16色順
  （`black`から`white`）の後に`#RRGGBB`、装飾は`bold`／`italic`／`underlined`／
  `strikethrough`／`obfuscated`の順とする。これは`LineValue.decorations`のtoken名昇順とは別のerror inventory順である。

block stateのJSON numberは十進数値としてscale非依存で比較する。`3`、`3.0`、`3e0`は同じnumber、
string`"3"`は別型とする。BlockValue出力はregistryの正準型を使い、整数stateをJSON integerへ戻す。

| family | code | reason | 意味 | 導入 |
| --- | --- | --- | --- | --- |
| ref 検証（protocol 21履歴） | `-32602`（Invalid params） | `malformed_ref` | 括弧崩れ等のparse失敗。protocol 22では使用しない | b4まで |
| block検証 | `-32602`（Invalid params） | `unknown_block` | `block_id`がblock不在（無印補完後の未知名含む） | ○ |
| | | `unknown_property` | property名がそのblockに無い | ○ |
| property検証 | `-32602`（Invalid params） | `invalid_property_value` | block state、sign色／装飾等の値が許容外。`allowed`を返せる | b1、signはb6 |
| params 検証 | `-32602`（Invalid params） | `invalid_params` | JSON-RPC params の形・型・座標値が不正 | b2 |
| | | `unknown_dimension` | 指定DimensionKeyがloaded dimensionとして解決できない | b5／protocol 22 |
| world-state | `-32000`番台（実装定義域） | `build_denied` | build policy / 範囲 / 認可により操作拒否。返せる場合は `data.bounds` / `data.violating` 等で理由を補足 | ○ |
| player-state | `-32000`番台（実装定義域） | `permission_denied` | LuckPerms 等の認可により操作拒否。token は温存 | b2 |
| | | `player_offline` | token は有効だが paired player がオンラインでない | b2 |
| | | `teleport_failed` | `player.setPose`等のteleport自体が`permission_denied`／`player_offline`／`unknown_dimension`／`invalid_params`以外の要因で失敗 | b5／protocol 22 |
| world-query | `-32000`番台（実装定義域） | `height_not_found` | 指定上限以下に「非passableかつ直上passable」のblockが無い | b5 |
| sign-state | `-32000`番台（実装定義域） | `not_a_sign` | 指定座標のblockがsignでない | b6 |
| | | `sign_waxed` | waxed signへのwriteを拒否。readは許可 | b6 |
| | | `sign_update_failed` | mutation時にstale snapshot等を検出し、部分変更なしでwriteを拒否 | b6 |
| resource-ref | `-32602`（Invalid params） | `unknown_particle` | canonical particle IDがregistryに無い | b5 |
| | | `particle_data_required` | b5では扱わないtyped data必須particle | b5 |
| | | `unknown_entity` | canonical entity IDがregistryに無い | b5 |
| | | `entity_not_spawnable` | playerまたはspawnを許可しないentity type | b5 |
| availability | `-32000`番台（実装定義域） | `backpressure` | 副作用開始前の一時的な処理能力超過。同一要求を後でretry可能 | b5 |
| | | `work_limit_exceeded` | 入力量または走査量がwork上限を超過。自動retryせず入力を縮小する | b5 |
| | | `entity_capacity_exhausted` | handle slotを副作用前に予約できない。自動retryしない | b5 |
| entity-state | `-32000`番台（実装定義域） | `entity_handle_not_found` | foreign／unknown handle。存在差を公開しない | b5 |
| | | `entity_removed` | known handleの対象entityが除去済み | b5 |
| | | `entity_unloaded` | known handleの対象entityがunloadされ現在操作不能 | b5 |
| | | `entity_dimension_changed` | 対象entityが外部要因でissued dimensionから移動 | b5 |
| | | `entity_spawn_failed` | admission後のspawn自体が失敗 | b5 |
| server-state | `-32603`（Internal error） | `internal_error` | 結果が確定できない。非冪等操作を自動retryしない | b5 |
| params 検証 | `-32602`（Invalid params） | `credential_not_found` | `auth.revoke` で指定した `credential_id` が要求元 UUID の active credential に無い（他 player の ID と存在しない ID を同値へ畳んで存在を隠す）。**caller の token は温存**し、`ref` に `credential_id` を返す | bN |
| credential-state | `-32000`番台（実装定義域） | `credential_limit_reached` | UUID ごとの active long-lived credential 上限に到達。`data.type` / `data.limit` / `data.active` を返す。古い credential を自動失効させず、ユーザーが list / revoke する | bN |
| auth-service | `-32000`番台（実装定義域） | `credential_store_unavailable` | server が credential 状態を現在検証できない、または credential 管理操作の durable な結果を確定できない。`data.operation`（`resolve`/`issue`/`list`/`revoke`/`touch`）を返す。**単独では token を invalid と分類せず、client は token を削除せず自動再ペアリングもしない**（token 温存・再試行） | bN |

- **`missing_namespace` は廃止**（無印は有効＝`2026-06-27-02`、`minecraft:` 補完される）。
- **`credential_not_found` と `token_not_found` は別物**（`2026-08-02-01`）：`token_not_found` は hello で提示した bearer token 自体が無効＝`2026-07-04-03` 項3 の**破棄・再ペアリング**側。`credential_not_found` は `auth.revoke` で指定した管理対象 ID が見つからないだけで、**caller の token は有効なまま**。`credential_store_unavailable` も温存側で、サーバー側の一時的な store 障害で全 client が有効な credential を捨てて再ペアリングへ雪崩れ込むことを防ぐ。プラグイン内部の線形化（authority commit の前後で何を返すか）は wire に出さず `11-plugin/platform-design_ja.md` が持つ。
- **reason 分割の理由**：生徒のミスが別物（付け忘れ/構文破壊/prop 無い/値不正）で、ライブ画面が別メッセージを出せると切り分け教育になる。`allowed` を返せるのは `invalid_property_value` だけ＝非対称が綺麗に出る。
- **`unloaded_chunk` は b1 reason から廃止**（DECISIONS `2026-07-01-08`）。未生成 chunk に対してロード/生成せず有意味な block 操作や query を行う実体はなく、許可された操作ならロード/生成して処理する。禁止すべき操作は chunk ロード状態ではなく build policy / 範囲 / 認可の問題なので、ユーザーに返す安定 reason は `build_denied` とする。chunk generation policy が必要になった場合は bN で別 reason として設計する。
- **後送り（名前予約のみ）**：`catalog_cache_stale`・`unknown_namespace`・`out_of_bounds`(world-state/y 範囲外・即判定で混乱しないため後送り)。
- **適用範囲**：b1 では getBlock に加え、chat.post/setBlock/setBlocks も **id 付き同期 request** として result/error を取れる形を基準にする（`2026-07-01-08`）。notification は JSON-RPC 上は可能だが result/error を返さないため、send-only 既定化は b1 の疎通確認対象から外す。server pushは採らず、eventは§5.4のpollへ進める（`2026-08-16-05`）。
- **送信モードの体験タクソノミー**はprotocol 22／b5でDEBUG／TRACE／FASTへ具体化した（`2026-08-20-03`）。wire上の実体はnotification（応答なし）、id付きrequest（同期result/error）、`connection.flush` barrierであり、mode名やdelayはwireへ送らない。TRACEはclient側pacing、FASTはsend-onlyで、batch／jobは引き続き高水準API・後続protocolの話である。

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

b1（protocol は clean な 21.0.0、配布物は `2100.0.0b1` 系）は **payload flip と疎通確認に徹し MVP を小さく切る**（versioning-design §10.11、DECISIONS `2026-06-25-05` / `2026-07-01-08`）。エラー往復は **id 付き request**（setBlock/setBlocks/chat.post の同期 result/error）または **getBlock**（常に request）で示す。send-only / notification 既定化は b1 の到達点に含めず後続へ送った。server push方向は後に`2026-08-16-05`でpollへ改訂した。

**b1 で通したい最小テスト:**

1. `hello` が成功する（安定応答・`protocol`=`21.0.0`・`catalogHash:null`・`world_constants.y_sea` key が存在、§6）。
2. `build.setWorld` / `build.setOrigin` が収容されている（Scratch b1 UI の `setOrigin` は固定値 `0` を見せ、y=0 固定で送る）。
3. `world.setBlock(...,"minecraft:stone")` が成功する。
4. `world.setBlock(...,"minecraft:oak_log[axis=y]")` が成功する。
5. `world.getBlock(...)` がfull・完全修飾の`"minecraft:oak_log[axis=y]"`を返す（protocol 21当時の正準形）。
6. 不正state・未知blockはid付きsetBlock/setBlocksで、build policy範囲外はid付きsetBlock/setBlocksまたはgetBlockで、対応する`data.reason`（`unknown_block`／`invalid_property_value`／`build_denied`等、§7.3）のerrorが返る。

**b1 でやらないこと**（当時の後送り）：全 block catalog 配信 / mod catalog 取得 / full `world_constants.json` 配送 / `y_sea` の完全な意味論・superflat 判定 / multi-version switching / Scratch 全 state UI / Scratch `setOrigin` の X/Y/Z 編集版・session/reconnect/save と origin 固定タイミングの厳密仕様 / Python 完全補完・`.pyi` 生成 / creative tab 再現 / ドア helper 実装 / kwargs 入力（catalog 連動・b2）/ サーバ→クライアント async error push。最後のpush方向は`2026-08-16-05`で採らず、event pollへ置き換えた。
