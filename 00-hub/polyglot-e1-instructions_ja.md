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

## 返却と照合（2026-11-10）

McRemote、Scratchとも、knowledge `fc3eeffef28acfa54d1c112751fe95fd4e587fdb`を読んだ。coordinatorがGitHubのAPIで、PR、merge commitと
既定のbranchの先頭、CIのrun、文書のbytesを確かめた。列は[Protocol Inventory](../10-protocol/protocol-inventory_ja.md)へ写した。

| 担当 | PR | merge commit | CI | 文書（bytes、SHA-256） |
| --- | --- | --- | --- | --- |
| McRemote | #15（head `8342936392e0d0c7c6484a452c964ea81bf00b90`） | `a38beaf121ce06594391237cb09745ec0da7649d` | run 42737576092（Build、手動、PRのhead。merge commitとtreeが同じ）、7 job成功 | `docs/polyglot-e1_ja.md`、23,811 bytes、`522f42d7e27b3cdd502b715a16cc8fc1479c83acde9169c892c18a7fafdd3881` |
| Scratch | #32（head `0ff5abdadda11b6b37f7156638d6449e2bcf8f82`） | `dc2840ba3c5c9d6938555ed737bc199acca2586e` | run 42737534055（PRのheadで全workspaceのbuildとtest）、merge後のrun 42743049672、どちらも成功 | `docs/polyglot-e1_ja.md`、19,675 bytes、`2b97a2169eef13695bfb151f48fa83cde6cdb2b4373002623fe39dd9628917ff` |

- どちらのPRも、変えたのは文書の1 fileだけ
- fixtureの取得元は、2つとも前から`21a2a9a`で、固定し直す差分は無かった。McRemoteはcopyの7本とLICENSEを、Scratchは
  取得したLICENSEを、bytesで確かめた
- McRemoteはmethod 32、auth 5、能力14に、能力5行を足した。Scratchは同じ行に、Scratch固有の投影3行とPhase Dの評価を足した
- McRemoteのF1への注意は、Inventoryの「E2への入力（2026-11-10）」へ入れた

