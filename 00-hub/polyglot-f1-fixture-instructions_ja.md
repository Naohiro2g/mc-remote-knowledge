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

## 返却と照合（2026-11-10）

tooling担当はknowledge `308a2a441060265e10af3d5e8e97c826c86b4ed8`を読んだ。PR #4（head `47926406f62925e589afaf5ca1c48ac43e3c5364`）を
merge commit `8264c3881bb4128c14cda6d122641ebcfa67d9c5`でmergeした。PRのCIはrun 42744132570、merge後のCIはrun 42744476837で、
どちらも成功した。coordinatorはGitHubのAPIで、PRとmerge、CIを確かめ、merge commitから9 fileを取ってbytesとSHA-256を
照合した（返却の値とすべて一致）。`df61e58`からの差分はこの9 fileだけで、既存の10本とLICENSEは変わっていない。

| file | case | bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `packages/protocol/test/fixtures/client-bootstrap-blocks-v23.2.1.json` | 12 | 45,945 | `664babdf3131a74e4aaf6d9e5dfb5e4cfc6e197df0a0d48142688820f1be813d` |
| `packages/protocol/test/fixtures/client-bootstrap-close-v23.2.1.json` | 6 | 14,535 | `44e9a4276bbd204671db0385f4f801cd3b152d0853ac943876ede73db6bd8dd1` |
| `packages/protocol/test/fixtures/client-bootstrap-errors-v23.2.1.json` | 3 | 9,179 | `c458d3ffbae846cfb33c032eba14d8f0005c6a1fbe871290b53fcfec8ec41aaa` |
| `packages/protocol/test/fixtures/client-bootstrap-framing-v23.2.1.json` | 7 | 15,131 | `be063b519b5d653a4bb4ec3da6f67e5d481a28dcf5913961c848b2b909d4b26d` |
| `packages/protocol/test/fixtures/client-bootstrap-hello-v23.2.1.json` | 9 | 18,734 | `0164639f946c58f1a2548334d6ff7032a50ec57dd797a328094eff7f104dc0a1` |
| `packages/protocol/test/fixtures/client-bootstrap-pairing-v23.2.1.json` | 7 | 19,322 | `cdb2209d8a1d46fede158db50c3672936dad152c7fd2bec7ef5a068ed57a1fe1` |
| `packages/protocol/test/fixtures/client-bootstrap-v1.schema.json` | — | 9,908 | `026d15c2d09f955ba47d6abd0c06a5af3e49ae41e4cc94441b4f0d9829b1d26f` |
| `packages/protocol/test/client-bootstrap-owner-fixture.test.ts` | — | 4,298 | `d9689e0203574e63c70a16e2f0be89757eef82731e81df754402b998598bcc50` |
| `packages/protocol/README.md` | — | 8,244 | `ec53c8c62746824413db65889e6127471667bdf3a94d31bb1f06228dc99e77cc` |

- toolingの見立て：hello→setBlock→getBlockの正常な流れを独立に作るためのデータはそろった。承認を拒む応答、closeの時の
  clientの振る舞い、browserとBridgeの境界、各言語のerrorとcredentialの使い勝手は、これだけでは決まらない
- McRemoteのE1の返却と突き合わせると、`protocol_mismatch`のcodeとdataが違う（McRemoteは`-32600`と`server`、
  `client_requires`、F1は`-32000`と`reason`だけ）。F1はこれを「未確定」としているので、E2で決める（Protocol Inventoryの
  「E2への入力（2026-11-10）」）
- 中身は[Protocol Inventory](../10-protocol/protocol-inventory_ja.md)の「F1のfixture（2026-11-10、toolingの返却）」と共有fixtureの列へ写した

