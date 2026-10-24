# 認証の操作と設定の整理（プレイヤー、運用管理者、開発）

> 状態：草稿（2026-10-25、coordinator）。human owner 2026-10-25「トークンの認証コマンド、管理コマンド、フラグについては、
> プレイヤー、運用管理者、開発のマトリクスで整理したい」。knowledgeに書いてあることだけで埋め、McRemoteとPythonにある
> はずで、knowledgeに無いものは「確認」とした。決定ではない。正本は`00-hub/authentication-roadmap_ja.md`と、
> そこに挙げた決定。

## 1. なぜ整理するか

long-lived credentialを本格化する（human owner 2026-10-24「セッショントークンもかなりこなれてきたので、次のステップとして」）。
ただ、long-livedがあると、clientが保存したtokenで自動でつながるので、sessionの振る舞いを確かめにくくなる。これまでは
sessionが約2時間で切れるので、切れた後のフレッシュな検証も、切れる前の継続の検証もできていた（human owner 2026-10-24）。

誰が、どこで、何を操作できるかを並べ、足りないものと、検証のための切り替えを見つける。

## 2. 役割

| 役割 | 誰か | 操作する場所 |
| --- | --- | --- |
| プレイヤー | 生徒、利用者 | Minecraftのチャット、client（Python、Scratch） |
| 運用管理者 | サーバーのoperator | サーバーのconsole、McRemoteの設定、LuckPerms、Stack |
| 開発 | McRemoteやclientを作り、確かめる人 | 上の全部と、試験のための設定 |

## 3. マトリクス

「今」はknowledgeに書いてある状態。「確認」は、あるはずだがknowledgeに無いもの。「案」は、まだ誰も決めていないもの。

### 3.1 認証（つなぐ）

| 操作 | プレイヤー | 運用管理者 | 開発 | 今の状態 |
| --- | --- | --- | --- | --- |
| ペアリング（`/mcremote pair <code>`） | 使う | — | 使う | 今。pair codeは約120秒、一回限り（`2026-08-22-01`） |
| tokenの種類を選ぶ（`auth.pairBegin`の`token_type`） | clientが選ぶ | — | 選び分けたい | 今は`session`が既定。Pythonは`long_lived`を既定にしない。Scratchは`session`だけ（`2026-08-07-01`②） |
| 保存したtokenで自動でつなぐ | client | — | 止めたいときがある | 今。保存したtokenがあれば、まずtoken付きhelloを試す（`00-hub/authentication-roadmap_ja.md` §1.1） |
| その実行で使うtokenの種類を選ぶ（保存したlong-livedを使わない等） | — | — | 使う | **案**（Python） |

### 3.2 管理（見る、消す）

| 操作 | プレイヤー | 運用管理者 | 開発 | 今の状態 |
| --- | --- | --- | --- | --- |
| 自分のcredentialの一覧（`auth.listCredentials`） | clientから | — | 使う | wireは批准済み（`2026-08-02-01`）。正式な管理面は後続（`2026-08-07-01`⑥(1)） |
| 自分のcredentialの失効（`auth.revoke`） | clientから | — | 使う | 同上 |
| 今のtokenを捨てる（`auth.logout`） | clientから | — | 使う | 同上 |
| PythonのCLI（`login`、`status`、`devices`、`revoke`、`logout`） | 使う | — | 使う | 未実装。今あるのは`mcremote init`だけ（`12-python-client/python-client-guide_ja.md`） |
| Minecraftのチャットで失効させる | ? | ? | ? | **案**。Scratchが管理の画面を持たないので、コマンドで足りるか（human owner 2026-10-24） |
| `/mcremote credentials reset` | — | 使う | 使う | **確認**。human owner：tokenの一括リセットができる。knowledgeに記述が無い |
| `/mcremote credentials bootstrap` | — | ? | ? | **確認**。knowledgeに記述が無い |
| `/mcremote credentials status` | — | ? | ? | **確認**。knowledgeに記述が無い |
| credential storeが欠けたときの新しいdomain | — | 起動ログで知る | 試す | 今。snapshotかauthorityが欠けていれば新しいdomainを作り、旧tokenを全部失効させる（`2026-09-25-01`） |
| Stack doctorでcredentialの健康を見る | — | 使う | 使う | checkpointが未実装の間は、doctorがfail closed（`00-hub/authentication-roadmap_ja.md` §2.1） |

### 3.3 設定（フラグ）

| 設定 | プレイヤー | 運用管理者 | 開発 | 今の状態 |
| --- | --- | --- | --- | --- |
| `auth.enforcement` | — | `true`のまま | 診断、移行の試験、特殊なclientの検証で一時的に`false` | 今（`2026-08-30-02`）。`false`ではtokenの無いhelloが通る。開発の既定にもしない |
| 受け付けるtokenの種類（`session`だけ／`long_lived`だけ／両方） | — | 選ぶ | 片方を止めて試す | **案**。外した種類は、新しく出さず、helloでも拒むか（human ownerに確認） |
| sessionの期限（約2時間） | — | — | 短くして切れた後を試す | **案**（coordinator）。開発のサーバーでだけ短くするか（human ownerに確認） |
| long-livedの期限、1人あたりの上限 | — | 選ぶ？ | 試す | 上限の到達は`credential_limit_reached`（wireの表で「bN」）。値と設定の場所は**確認** |
| 建築の権限（`mcr.online`、`mcr.offline`、build range） | — | LuckPermsで決める | 試す | 今（`2026-09-01-02`） |

## 4. 見えてきたこと（草稿）

- 開発の切り替えは、サーバー（受け付ける種類、期限）とclient（その実行で使う種類、tokenを捨てる）の両方に要る。
  サーバーだけなら、clientに何が保存されていても、そのサーバーではsessionだけの検証ができる。clientだけなら、同じPCで
  両方を行き来できる。
- 運用管理者のコマンド（`/mcremote credentials`）はMcRemoteにあるが、knowledgeに無い。
- プレイヤーの管理（一覧、失効、logout）は、wireはあるが、使う入口（Python CLI、チャットのコマンド）が無い。
- long-livedの再開は、`2026-08-07-01`⑤（実利用で需要が確認されてから。開発者の便宜だけを需要の証拠にしない）を
  改める横断決定になる。

## 5. 次の操作

- 初回stableの後（11/2〜7）に、McRemoteとPythonへ確認票を出し、「確認」の行を埋めてもらう。McRemoteには
  `2026-08-02-03`の再開トリガ(1)〜(5)、Stackには(6)の状態もあわせて聞く。
- 「案」の行は、human ownerが採るかを決める。
- 埋まったら、long-livedの再開の決定と、`2321.1.0`か`2330.0.0`の範囲に入れる。
