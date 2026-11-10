# 各clientのCIでF1のfixtureを通す依頼（F3、Python・Java）

> 多言語Client LibraryのPhase E／F（`2026-10-23-01`、`10-protocol/polyglot-phase-ef-plan_ja.md`の「F3」）。F3の合格は、
> 各clientのCIでF1のfixtureが全件PASSし、実McRemoteを相手にしたpulseが1本通ること。human owner 2026-11-10：
> 「クライアントの多言語化を最優先とする。その先のUnity版マイクラリモコンを急ぐため」。この票は、各担当の受け持ちの中で
> 先にしてください。参照するknowledge commitは、この依頼が入ったmainのcommitです。Python担当は「共通」と「Python」、
> Java担当は「共通」と「Java」を読んでください。

## 共通

- 対象：minecraft-remote-tooling `8264c3881bb4128c14cda6d122641ebcfa67d9c5`の`packages/protocol/test/fixtures/`にある、F1の6本
  （`client-bootstrap-{framing,hello,pairing,blocks,errors,close}-v23.2.1.json`、44 case）と、schemaの
  `client-bootstrap-v1.schema.json`。scripted peerのデータの形は、同じcommitの`packages/protocol/README.md`にある
- toolingが、`protocol_mismatch`のcaseを`2026-11-10-01`に合わせる（F1-HE-09のdataに欄を足し、`-32600`で届くcaseを1つ足す。
  `00-hub/polyglot-f1-mismatch-fixture-instructions_ja.md`）。そのmerge commitをcoordinatorから伝えるので、同じPR（mergeして
  いれば次のPR）で取得元を固定し直す。それまでは`8264c38`で進めてよい
- 読み方：固定したcommitで読む（F2）。copyで持つときは、同じディレクトリの`LICENSE`（1,070 bytes、SHA-256
  `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）も一緒に置く。共通のtest runnerは作らず、自分の言語の
  test runnerでloaderを書く
- `client-bootstrap-blocks-v23.2.1.json`の12 caseは、`value_refs`で同じディレクトリの`block-value-v22.json`を参照する。
  今つないでいなくても、その参照の範囲で読む
- 合格：CIで、F1の全caseがPASSする。skipを残したら、F3は済みにしない。caseが契約と違う、または読み方が決まらないと思ったら、
  そのcaseのIDと理由を返す（coordinatorがtoolingへ回す）
- `unresolved`を持つcaseは、`expected`に書いてあることを確かめる。`unresolved`に挙げたこと（EOFの時の扱い、応答待ちの
  requestの例外の型とtimeout、自動の再送など）は、clientで新しく決めない。決める必要が出たら、決めずに返す（E2で決める）
- `protocol_mismatch`は`data.reason`で判定し、codeでは分けない（`2026-11-10-01`）。`data.server`と`data.client_requires`は、
  errorから読めるように保つ
- caseに合わせてclientの振る舞いを直してよい。直したことは返却に書く。振る舞いを直すときは、そのcaseが直す前に意図した理由で
  落ちることを見てから直す
- 実McRemoteとのpulse：hello → `world.setBlock` → `world.getBlock`を1本通す。相手は、担当の手元のPaperと、公開のMcRemote
  `2321.1.0`。認証は、今あるlive testの方法を使い、その方法を返す。Minecraftの中での承認など、人の操作が要るなら、その前で止めて
  手順を返す（human ownerが行う）。token、pair code、host、IP、player名、座標は返却に書かない
- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。tag、Release、公開のworkflowの実行はしない

## Python

- 応答の版の互換判定を入れる（`10-protocol/versioning-design_ja.md`の「8.2 互換判定（クライアント側）」）。majorの一致、
  serverのminorが同じか上、patchは見ない。F1のF1-HE-04〜08が、その期待値（04と05は不一致、06〜08は一致）
- 不一致は、`Minecraft.create()`の失敗（`2026-08-02-06`⑤の「protocol mismatch」）にする。tokenは消さない（`2026-08-30-03`）
- 申告するprotocolは今の`23.2.1`のまま

## Java

- Javaが要求する最低のprotocolは`23.0.0`で、F1のhelloのcaseは、clientの申告を`23.2.1`としている。testでは、caseの申告の値を
  使ってよい。Javaの既定の申告を変えるかは、変えずに、案と理由を返す（human ownerが決める）

## 返却

- PRの番号、merge commit、CIのrun ID
- fixtureの取得元の前と後（commit、copyならbytesとSHA-256）
- fileごとのcase数とPASS数。直したclientの振る舞い（caseのIDと、前と後）
- 違うと思ったcaseと理由、決めずに残したこと
- pulse：日付、Paperの版、McRemoteの版（`2321.1.0`）、手順、結果。認証の方法
- Protocol Inventoryの「共有fixtureの使い方」の自分の行の、前と後
- Javaだけ：既定の申告のprotocolの案

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、fixtureのbytes）で照合し、Protocol Inventoryへ写す
- toolingの返却のmerge commitを伝える
- 違うと思われたcaseをtoolingへ回し、決めずに残されたことをE2の案に入れる
- TypeScriptの実装を始める票を作る
