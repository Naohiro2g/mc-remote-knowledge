# 新しいclientが作れるだけの共有fixtureを足す依頼（F1、tooling）

> 多言語Client LibraryのPhase E／F（`2026-10-23-01`、`10-protocol/polyglot-phase-ef-plan_ja.md`の「F1」）。human owner
> 2026-11-10：「クライアントの多言語化を最優先とする。その先のUnity版マイクラリモコンを急ぐため」。F1の範囲がそろったら、
> TypeScriptの実装を始める。tooling担当は2026-11-06に、今の10本では新しいclientがhelloからsetBlock／getBlockまでを独立に
> 作れないことと、追加の案を返した（minecraft-remote-tooling `1286eb486bcaea93c4195c11e94304bdb51f53ba`の
> `packages/protocol/FIXTURE_INVENTORY_ja.md`の「3. F1の不足と追加案」）。この票は、その案のとおりにfixtureを足す依頼です。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 範囲

対象のprotocolは`23.2.1`。返却の案の6行を、すべて入れる。

| 範囲 | 足すもの | 期待値の根拠（`10-protocol/wire-format-design_ja.md`） |
| --- | --- | --- |
| framing | UTF-8の改行区切りJSON、分割受信、複数行の結合受信、未完の末尾、idの対応 | 「2. トランスポートとフレーミング」、「3.4 id 規律」 |
| hello／negotiation | helloのparamsとresult、protocolの一致と不一致（majorの不一致、serverのminorが足りない、patch）、`protocol_mismatch` | 「6. helloペイロード」、`10-protocol/versioning-design_ja.md` |
| authentication／pairing | `auth.pairBegin`→Minecraftでの承認に当たる段→`auth.pairPoll`→tokenつきのhello。pending、期限切れ、拒否、tokenの再利用 | 「6.5 認証：ペアリングフロー」、「6.6 credential 管理」 |
| `world.setBlock`／`world.getBlock` | requestとresponseの全体、既定のstateと明示したstate、正準化、namespace、不正なstateの拒否。値は既存の`block-value-v22.json`を参照してよい | 「4. コマンド表（確定）」、「7.1 構造化block value」、`10-protocol/block-value-design_ja.md` |
| errorの外枠 | JSON-RPC errorの`code`、`message`、`data.reason`、requestとの対応、知らないreasonを保つ例 | 「3.3 応答」、「7.3 エラー設計」 |
| close | 正常なclose、EOF、行の途中でのEOF、つながらない、応答待ちのrequestがある時のclose、新しい接続でのhelloのやり直し | 「2. トランスポートとフレーミング」 |

- 送受信の順を再生するcase（scripted peer：`client → hello`、`peer → protocol_mismatch`など）は、データとして書く。形はtoolingが
  決め、`packages/protocol`のREADMEに書く
- tokenは、fixture用に決めた値を使う。本物のcredentialは使わない
- 契約に書いていないことに出会ったら、fixtureで決めない。返却に「未確定」として挙げる（E2で決める）。自動の再送の採否も
  fixtureで新しく決めない
- 置き場所は`packages/protocol/test/fixtures/`（MITのLICENSEのあるディレクトリ）。共通のtest runnerは作らない（F2）。
  toolingのCIでは、fixtureのJSONの形と、caseどうしの参照が切れていないことを確かめる

## 進め方

- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。clientは固定したcommitで読むので、直しは後のcommitで出せる。
  tag、Release、公開のworkflowの実行はしない
- McRemote担当が、同じ時期にE1の票（`00-hub/polyglot-e1-instructions_ja.md`）で、この案とserverの振る舞いの違いを返す。
  違いが分かったら、coordinatorから伝える

## 返却

- PRの番号、merge commit、CIのrun ID
- 足したfileの一覧（file名、case数、範囲、SHA-256）
- scripted peerのデータの形の説明（READMEのどこか）
- caseごとの期待値の根拠（wire-format-designの節）。根拠が契約に無かったもの（「未確定」）の一覧
- 新しいclientが、これだけでhelloからsetBlock／getBlockまで作れるかの見立て。足りないものが残れば、その一覧

## coordinatorがすること

- 返却をGitHubのAPI（PR、merge commit、CI、fileのbytes）で照合し、Protocol Inventoryの共有fixtureの列を直す
- 「未確定」をE2の案に入れる
- F3（各clientのCIでF1のfixtureが全件PASSし、実McRemoteとのpulseが1本通る）のため、Python、Javaへ、fixtureをつなぐ票を作る。
  TypeScriptの実装を始める票も作る
