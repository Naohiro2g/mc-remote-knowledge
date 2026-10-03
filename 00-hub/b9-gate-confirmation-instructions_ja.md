# b9横断release gate 確認票依頼

> b9横断release gate（`00-hub/release-gate-notes_ja.md`の2026-10-04の節）を開いたときに、各担当へ出す確認票の依頼です。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は、自分の節と「共通」を読んで確認票を返して
> ください。b9はAPIを変えません（protocol `23.2.0`のまま、artifact `2320.0.0b9`、`2026-09-30-03`）。

## 共通

返却は`release-gate-notes_ja.md`の確認票の形式。`knowledge contract commit`には実際に読んだSHAを書く。
自repoの事実と根拠だけを返し、他repoへの着手、shared環境の変更、人間参加の試験、tag／releaseの公開はしない。

移管（Protocol／WireScope／Bridgeのowner）は、topologyと範囲をhuman ownerがまだ決めていない。この票では調べて返すだけで、
repositoryの作成や操作、sourceの移動、取得経路の変更はしない（`2026-09-13-02`、移管計画の「再開gateと完了条件」）。

各担当に共通で聞くこと:

- b8の公開後に、mainまたはdefault branchへ入ったもの（commitと一行の説明）。b9で出すつもりのもの
- 契約2件（`2026-10-03-01`、`2026-10-03-02`）について、下の各節の問い
- READMEの人間向け再編（hub NOTES 2026-08-28 `[priority]`）で残っているもの
- 10/10に対する見込みと、止まっている点

## McRemote

- id付き`chat.post`の成功時に、今は何をresultとして返しているか。`null`に変えるとき、変わるのはどこか（`2026-10-03-01`）
- JARのunix権限bitの固定（hub NOTES 2026-10-03）: Gradleのjarの作り方をどう変えるか。手元とCIで同じdigestになることを、
  どう確かめるか
- 移管の材料: 共有fixtureを今どこへどう取り込んでいるか（path、copyかsubmoduleか、どのtestがdigestを見ているか）。
  取得元をScratchから別のrepositoryへ変えるとき、変える箇所と手間
- 移管の材料: scratch-editorのrepo名やURLを直接書いている箇所

## Python client

- `events.poll`の応答に、知らないevent typeが入っていたときの今の扱い（失敗するか、捨てるか、そのまま渡すか）。
  `2026-10-03-02`に合わせるとき、省略とopaqueのどちらにするか
- id付き`chat.post`の成功resultを、今どう扱っているか（`null`になっても壊れないか）
- PyPIへの登録の準備（`2026-09-26-03`、`2026-09-29-02`、versioning-design §10.9）:
  - b9のwheel／sdistを、正式段階の固定triggerからTestPyPIへ出せる状態か
  - 遷移ゲート①〜④のうち、b7.post3のsoakで済んだものと残るもの。④のWindowsはhuman ownerが確かめる
  - PyPI.orgへ出すときに、human ownerが行う外部の操作（project、trusted publisher、tokenなど。実値は書かない）
- 移管の材料: 共有fixtureの取り込み方、同梱WireScopeの作り方（`bundled_wirescope_source_commit`）、scratch-editorを
  直接書いている箇所。取得元が別のrepositoryへ移るときに変える箇所と手間

## Scratch editor（WireScope）

Scratchは移管の現ownerなので、調べる範囲が広くなります。移管計画の「再開時に評価する範囲」と「有力なtopology」、
人間向け固定文を読んでから返してください。

- 移管の材料（b8 closeのfixture一覧`14-evidence/artifacts/2026-10-03-b8-dev-live/scratch/2026-10-03-b8-close-inventory/FIXTURES_ja.md`
  を起点に）:
  - `@mc-remote/protocol`、WireScope（`mc-remote/live`）、Bridge（`mc-remote/bridge`）が、Scratch VM／GUIとbuildの
    どこでつながっているか。repoの外へ出すと切れるもの
  - topologyの候補ごと（共通TypeScript tooling monorepo、Protocol repo＋WireScope repo、Hybrid）に、移す範囲、
    Scratch側に残るもの、CIとrelease workflowの変え方、手間の見込み。公開済みの`Naohiro2g/minecraft-remote-protocol`
    （park中）を使う場合と使わない場合
  - Bridgeを維持、一般化、Scratch専用への縮小、廃止のどれにするかの材料（誰が使っているか、他の経路で置き換えられるか）
  - 取得経路の候補（npm、Git commit pin、vendor、生成物）と、Scratchのbuildがどれなら回るか
  - rollbackのやり方（b8の`691576f`へ戻すときに、何を戻せばよいか）
  - 推奨するtopologyと、その理由。10/10までに収まる範囲と、収まらない部分
- 知らないevent typeの扱い（Scratch VMとWireScopeのそれぞれ）。`2026-10-03-02`に合わせるときに変える箇所
- shared fixtureに、契約2件のcase（`chat.post`のresult `null`、知らないevent typeを含むpoll）を足せるか
- WireScopeの列幅（`agent/b8-compatibility@01cdb0b`）: そのままb9に入れてよいか
- b8の後に残ったものの状態: pickerのalias検索（何をaliasとして登録するか、その出どころ。名前データは公式の言語データの
  最小限だけという`2026-09-30-10`との関係）、b7 release後の是正候補3件のうちb8で終わらなかったもの（backpressureの案内など）
- protocol 22 Scratch block value投影の残り（hub NOTES 2026-08-19のpark行。名前データの置き場所とexact schema、
  一段／二段表示など）の状態

## Java client（gateの条件にしない）

Javaはb9に参加しません（`2026-09-30-04`）。返却はb9 gateの判定に使わず、freezeと移管の前に知っておくために聞きます。
返却は確認票の形式でなくてよく、次の2点だけを返してください。

- freeze前の契約の疑問点: 契約監査で返した2件（`2026-10-03-01`、`2026-10-03-02`）のほかに、APIを固定する前に決めておく
  べき疑問点が残っているか。棚卸しはこれで終わりか、まだ続いているか。残っていれば、10/10の前に搬送票で返す
- 移管の影響: 共有fixtureを今どう持っているか（手元のcopyか、scratch-editorのrepoやpathを直接参照しているか）。
  Scratchのfixtureのpathやrepositoryが変わったときに、JavaのbuildやCIが切れる箇所があるか
