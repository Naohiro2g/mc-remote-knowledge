# Protocol InventoryのMcRemoteとScratchの列を返す依頼（E1）

> 多言語Client LibraryのPhase E／F（`2026-10-23-01`、`10-protocol/polyglot-phase-ef-plan_ja.md`）のE1で、
> [Protocol Inventory](../10-protocol/protocol-inventory_ja.md)のPython、Java、共有fixtureの列は2026-11-06に返った。残りは
> McRemoteとScratchの列。human owner 2026-11-10：「クライアントの多言語化を最優先とする。その先のUnity版マイクラリモコンを
> 急ぐため」。この票は、各担当の受け持ちの中で先にしてください。参照するknowledge commitは、この依頼が入ったmainのcommitです。
> McRemote担当は「共通」と「McRemote」、Scratch担当は「共通」と「Scratch」を読んでください。

## 共通

- 基準は公開の`2321.1.0`のtag（McRemote `5b78ded96d1ad6d45160b67c5f8a13e14adb3fc8`、Scratch
  `57fb7691bb5d9a5895785b200ae78734240ebfa6`）。既定のbranchと違うところがあれば、それも書く
- 行：Protocol Inventoryの「method」の32、「auth」の5、「methodでない能力」の各行。表に無い能力を持っていれば、行を足して返す
- セル：「あり」「部分」「なし」と、根拠（file、class、test名）。「あり」は投影や実装があることで、全reasonや実機の全経路を
  確かめたことではない。確かめていないことは、そう書く
- 「共有fixtureの使い方」：今testへつないでいるfixtureと、つないでいないfixture
- fixtureの取得元の固定し直し：取得元をminecraft-remote-tooling `21a2a9a0aed8b4d9c715da46616aad86f1174b4c`の
  `packages/protocol/test/fixtures/`にする。fixtureの10本は、それまでの`6447f6e`とbytesが同じ。copyで持つときは`LICENSE`
  （1,070 bytes、SHA-256 `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）も一緒に置く。toolingの`main`は、
  その後fixtureを変えていない
- 書く場所：Python、Javaと同じく、自repoの`docs/polyglot-e1_ja.md`（置けなければ、置いた場所を返す）
- 変えるのは、その文書とfixtureの取得元だけ。既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。tag、Release、
  公開のworkflowの実行はしない
- 返却：PRの番号、merge commit、CIのrun ID、文書のpath、fixtureの取得元の前と後、CIでつないだfixtureがPASSしたこと

## McRemote

- 列の意味：serverがそのmethodや能力を受けて処理するか。reasonで拒むものは、そのreasonも書く
- toolingのF1の不足と追加案（minecraft-remote-tooling `1286eb486bcaea93c4195c11e94304bdb51f53ba`の
  `packages/protocol/FIXTURE_INVENTORY_ja.md`の「3. F1の不足と追加案」）を読み、serverの今の振る舞いと違うところがあれば返す。
  F1は、新しいclientがhelloからsetBlock／getBlockまでを独立に作れるだけのfixture（framing、hello／negotiation、
  authentication／pairing、`world.setBlock`／`world.getBlock`の対話、JSON-RPC errorの外枠、close）

## Scratch

- 列の意味：Scratchのblockや拡張機能の振る舞いへの投影があるか。根拠には、blockの名前とsourceのfileを書く
- Scratchは、Bridgeを通ってWebSocketでつなぐ。「WebSocket／browser」の行は、その経路を書く
- Scratchのclose返却の②の、共有fixtureの2つ（gateの後のfixtureの付け直し）を使ってよい

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、文書のcommit）で照合する
- 2つの列をProtocol Inventoryへ写し、E2（分類と未確定の判断）の案を作る
