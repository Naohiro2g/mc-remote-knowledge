# Phase E2：分類と未確定の判断（案）

> 状態：coordinatorの起案（2026-11-11）。未批准。E2は、[Protocol Inventory](protocol-inventory_ja.md)の各行を
> ロードマップ「14. Phase E」の分類に分け、未確定を決める段（`2026-10-23-01`、[Phase E／Fの案](polyglot-phase-ef-plan_ja.md)の「E2」）。
> 最初の判断として、`protocol_mismatch`の形は`2026-11-10-01`で決めた。この文書は残りの案。批准された部分は
> DECISIONSと、wire等の拘束層へ移す。

## 要約：決めてほしいこと

| # | 問い | 案 |
| --- | --- | --- |
| U1 | 人が承認を拒んだことを伝える専用の応答（`pair_denied`）を持つか | 今は持たない。拒否は、pendingのまま期限が切れて`pair_expired`になる |
| U2 | 接続が閉じた時、応答待ちのrequestをどうするか | すべて、localな「完了不明」の失敗にする。LFの無い末尾は捨てる |
| U3 | 応答待ちのtimeout | 各clientが持つ。timeoutは「完了不明」で、その接続を回収する |
| U4 | 自動の再送 | Client Libraryは自動で再送しない |
| U5 | 自動の再接続と再認証 | Client Libraryは自動で再接続しない。再接続は明示の操作で、新しいhelloから |
| U6 | serverが不正な行にerrorを返さないこと | 契約にしない。clientはLFで送り、errorが来ないことはtimeoutで扱う |

U2〜U5は、TypeScriptとC#がこれから作るところで、PythonとJavaは今、決めずにいる。U1〜U6は、どれも新しいwireを足さない。

## 1. 分類

ロードマップの分類の「Python固有」「Java固有」は、TypeScript、C#、Scratchが加わったので「言語固有」とまとめる。

### method

metadataの32 methodとauth節の5 methodは、すべてProtocolである（wireの「4. コマンド表（確定）」と「6.5」）。どのClient Libraryが
どこまで投影するかは各Client Libraryの進度で、全部を投影することは求めない（ロードマップ「33. このロードマップが作らないもの」の
「全Client APIの形状統一」）。

### methodでない能力

| 能力 | 分類 | 根拠と補足 |
| --- | --- | --- |
| TCPのframing／JSON-RPC | Protocol | wire「2」「3」。LF（`\n`）終端。McRemoteがCRLF／CRも受けるのはserverの寛容さ（U6） |
| WebSocket／browser | Protocol（1 WS message＝1 JSON）＋Application（Bridge） | wire「2」。BridgeのOriginとallowlistはPhase H |
| protocol negotiation | Protocol | versioning「8」。clientの側の判定も全clientが持つ（Pythonは2026-11-10に入れた） |
| authentication／pairing | Protocol＋Client共通意味論 | wire「6.5」がProtocol。「まずhello、`auth_required`のときだけpairing」はClient共通（`2026-07-04-06`の(c)） |
| session credentialのUX | Client共通意味論＋言語固有 | 共通の規則は`2026-08-30-03`。保存のbackendは言語固有 |
| request／notification／flushと順序 | Protocol＋Client共通意味論 | wire「3.5」がProtocol。DEBUG／TRACE／FASTのmodeはClient共通（`2026-08-20-03`） |
| events cursor／loss | Protocol | `events.poll`の契約 |
| error reason | Protocol＋Client共通意味論＋言語固有 | codeとreasonの二層はProtocol（wire「7.3」）。知らないreasonを保つこと、reasonから各言語の案内を作ることはClient共通。例外の型は言語固有 |
| build context | Protocol | wire「5」。ScratchのYを0に固定する投影は言語固有（Scratch） |
| BlockValue／BlockSpec | Protocol＋言語固有 | 値と正準化はProtocol（block-value-design）。値を組み立てるAPIは言語固有 |
| catalog／constants | Protocol＋言語固有 | `catalog.get`と`catalogHash`はProtocol。生成する定数と補完は言語固有（Phase D） |
| helloの`world_constants` | Protocol | wire「6.2」 |
| epoch／reconnect | Protocol＋Client共通意味論 | 新しいTCPは新しいepochでhelloから、はProtocol。再接続の時にcursor、cache、handleを捨てることはClient共通。自動の再接続はU5 |
| WireScopeのobserver | Application | `15-wirescope/` |
| 接続の前の資源とadmission、tickの実行量と公平さ、失効を永続させるcredential | serverの実装 | Client Libraryの分類の外。clientに見えるのはreason（`backpressure`、`work_limit_exceeded`など）だけ |
| resource IDの正準化 | Protocol | 正準の出力（wire「5.0.2」）。McRemoteの実装はserverの側 |
| ゲーム内の座標・時刻HUD | Application | protocolの外 |
| Scratchの3行（結果の変数とリストへの投影、block picker、モニターのpollを抑える） | 言語固有（Scratch） | Scratchの返却のとおり |

## 2. 未確定の案

### U1. 承認を拒む専用の応答

- 今：契約に無い。McRemoteは拒否の操作を持たず、承認されなければpendingのまま期限が切れる。F1は`unresolved`とした
- 案：今は足さない。clientは`expires_in`まで待ち、`pair_expired`で「承認されなかったか、期限が切れた」と案内する
- 理由：足すには、Minecraftの中の拒否の操作と、wireの変更（新しいreasonか`result.status`の値）が要る。学習者に返す案内は、
  今の`pair_expired`でも書ける
- 却下：今`pair_denied`を足す（McRemoteの操作とprotocolの版が要る）
- 再開：学習者向けのerror診断（hub NOTES 2026-11-10「学習者が直し方まで分かるエラー」）と同じく、次のprotocolの版の範囲を決めるとき

### U2. 接続が閉じた時の、応答待ちのrequest

- 今：wireの「3.4 id 規律」と「9. 既知ギャップ」は、切断の時の保留の解決を「要決定」としている。F1のclose（CL-03、CL-05）は、
  応答が来ていないという観測（`unanswered_ids`）だけを持つ
- 案（Client共通意味論）：接続が閉じたら、応答待ちのrequestをすべて、localな「完了不明」の失敗にする。serverのerrorとしては
  扱わず、reasonを作らない。LFの無い末尾は、JSONとして閉じていても応答にしない。例外の型は言語固有
- 理由：wire「3.5」は、flushのtimeoutを「serverから返されたJSON-RPC errorではなく、localな完了不明」としている。同じ考え方を
  closeへ広げる。応答待ちが切断でhangすることを防ぐ。Javaは既にこの形（`TransportException`、`unanswered`）
- 却下：①応答待ちを放置する（hangする） ②serverのerrorに似せたreasonを作る（serverが返していない結果を捏造する）

### U3. 応答待ちのtimeout

- 今：wire「3.5」は、flushについて「別のmagic timeoutを作らず、同じconnectionの通常のrequest timeoutを適用する」とし、timeoutでは
  「非冪等操作を自動retryせず、mode切替を成立させず、当該connectionを回収する」とする
- 案（Client共通意味論）：各clientは通常のrequestのtimeoutを持つ。値と設定の仕方は言語固有。timeoutはU2と同じ「完了不明」で、
  その接続を回収する（flushの規則を、すべてのrequestへ広げる）
- 理由：id付きのrequestの完了が分からないまま同じ接続を使い続けると、遅れて届く応答と次のrequestの対応が崩れうる
  （`2026-08-02-06`⑥と同じ懸念）。接続を回収すれば、言語によらず同じ扱いになる
- 却下：timeoutの後も接続を使い続ける（idごとの応答待ちの表があれば遅い応答は捨てられるが、server側で処理が続いているかは
  分からず、build stateの扱いが言語ごとに分かれる）

### U4. 自動の再送

- 案（Client共通意味論）：Client Libraryは、requestを自動で再送しない。`backpressure`は「同一要求を後でretry可能」
  （`2026-08-16-07`）だが、再送するかはapplicationが決める
- 理由：非冪等の操作（setBlocks、spawnEntityなど）を二重に実行しうる。Pythonは既に、`backpressure`以外のreasonを自動でretryしない
  （`12-python-client/python-client-guide_ja.md`）
- 却下：`backpressure`だけ、Client Libraryが自動で再送する（言語ごとに回数と間隔が分かれ、学習者が観察する重さが隠れる）

### U5. 自動の再接続と再認証

- 案（Client共通意味論）：Client Libraryは自動で再接続しない。再接続はapplicationの明示の操作で、新しいepochのhelloから始める。
  build state（dimension、origin）は接続ごとなので既定へ戻り（`2026-06-24-01`）、cursor、event cache、entity handleは捨てる
- 理由：自動で再接続すると、build stateとhandleが黙って変わる。Pythonの`reconnect()`も明示の操作
- 却下：切断を検知したら自動で再接続して同じ操作を続ける（原点が既定へ戻ったまま建築が続く）

### U6. serverが不正な行にerrorを返さないこと

- 今：McRemoteは、壊れたJSONや不正なidにJSON-RPC errorを返さず捨てるか、helloの前なら切断する。notificationにはerrorを返さない
  （McRemoteのE1の返却）
- 案：契約は今のまま（LF終端、notificationは応答なし）。不正な行にerrorを返すかは、serverの実装に任せて契約にしない。clientはLFで送り、
  errorが来ないことはU3のtimeoutで扱う
- 却下：serverに`-32700`／`-32600`のerrorを必ず返させる（壊れた入力への応答を増やすと、認証前の資源制限と衝突しうる）

## 3. E2では決めないもの

- 学習者向けのerror診断と、適用中の権限と上限の照会（`10-protocol/learner-error-diagnostics-notes_ja.md`）：新しいreason、data、
  helloの欄、methodを足すかどうかなので、Protocolの候補として分類だけする。次のprotocolの版の範囲を決めるときに判断する
- 公開のScratchのブロック一覧の古いmethodの名前：分類の問題ではない（hub NOTES 2026-11-10の行）
- `auth.pairBegin`の`client`の情報：情報用で、serverが保存や表示をしなくてよい（今のMcRemote）。契約を変える必要はない

## 4. 批准されたら

- U2〜U5：DECISIONSに1行。wireの「3.4 id 規律」と「9. 既知ギャップ」の該当の項を直す。F1のcloseのcaseの`unresolved`を、
  toolingへの票で決まったことに合わせる
- U1、U6：DECISIONSの同じ行に入れ、U1の再開をhub NOTESに置く
- PythonとJavaへは、次の票で、決まったこととの違いを返してもらう。TypeScriptとC#は、最初からそれに合わせる
