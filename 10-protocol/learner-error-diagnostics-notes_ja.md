# 学習者向けのエラー診断、権限の照会、FASTの性能とJARの配り方の検討メモ

> 状態：未決定の検討メモ。reasonの名前、APIの名前、専用JARの採用は決めていない。protocolの版も決めていない。
> hub NOTESの3行（2026-11-10の「学習者が直し方まで分かるエラー」「適用中の権限と上限を照会する」
> 「FASTの性能と、専用JARを統一JARより優先する可能性」）の参照先。
>
> 出典：2026-11-10にhuman ownerが貼った相談の文（下の「相談の原文」）。human owner：「学習者視点でエラーメッセージを
> 改善するアイデアを収録してください。polyglotプロジェクトにも関わる」。原文は、表と箇条書きの記号をMarkdownに直しただけで、
> 文には手を加えずに収めた。
> 「既存の記録との関係」はcoordinatorが足した。

## 既存の記録との関係

### 1. エラーの原因

- wire「7.3 エラー設計」の表は、`build_denied`について「返せる場合は`data.bounds`／`data.violating`等で理由を補足」とする。
  `13-scratch-client/debug-session-design_ja.md`の「building 制限の wire 部分（`build_denied` 方針メモ）」は、
  all-or-nothingを保ったまま、許可範囲`bounds`とはみ出した座標`violating`をerrorのdataで返し、画面に見せる案を書いている。
  原文の案は、これに加えて、対処が違う原因をreasonでも分ける
- player別の1操作の量の上限は、LuckPermsのmeta`mcr.build.blocks`で、超過は既存の`build_denied`で拒否する
  （`2026-10-07-05`、`11-plugin/platform-design_ja.md`の`default_build_blocks`の段）。
- `work_limit_exceeded`は「入力縮小が必要な拒否」で、clientは自動で再送しない（`2026-08-16-07`、
  `11-plugin/platform-design_ja.md`、`12-python-client/python-client-guide_ja.md`）
- Scratchは、allowlistにある`data.reason`だけを同じ名前のErrorTextへ写し、未知のreasonは`remote_error`へ畳む。messageと
  任意の`error.data`はErrorTextへつながない。command blockのserver errorを分岐できる結果に変えることは、その時のsliceに
  含めなかった（`13-scratch-client/scratch-block-value-projection-design_ja.md`、`2026-08-19-04`）
- 多言語Client Library：E2でerror reasonを分類する（`10-protocol/polyglot-phase-ef-plan_ja.md`の「E2」）。F1の
  `client-bootstrap-errors-v23.2.1.json`は、知らないreasonを保つ例を持つ（[Protocol Inventory](protocol-inventory_ja.md)の
  「F1のfixture」）。新しいreasonは、共有fixtureと各clientを合わせて入れることになる

### 2. 権限と上限の照会

- helloの`permissions`は`{online, offline, buildRange}`で、認証済みhelloの時に一度解決したsnapshotを返す（`2026-09-01-02`、
  wire「6.2 応答 `result`」）
- helloは、1操作の設置数の上限を返さない。`mcr.build.blocks`を入れた時の`11-plugin/platform-design_ja.md`の文
  「helloのpermissionsは変えない」は、実装の範囲の説明で、理由の記録は無い。2026-11-10に、規則として読める書き方を改めた

### 3. FASTの性能とJARの配り方

- 単一JAR：`2026-10-07-03`で、複数のMinecraft版で同じJARを使い、対象ごとに同じSHA-256のJARを検証すると決めた。
  `2026-07-04-05`の「必要ならmc-targetごとにartifactを分ける」は、b10から改めた。原文の案は、性能を理由に分ける可能性を残す
- hub NOTESの関係する行：2026-10-17「McRemoteの対応版を各系列の最終版へ広げる検討」、2026-10-24「Minecraft 26.4への移行」
- FASTはidなしのnotificationで、serverの個々のerrorは返らない。`connection.flush`の成功は、個々のnotificationの成功を
  集めない（`2026-08-20-03`、wire「3.5 build execution modeと`connection.flush`」）

---

## 相談の原文

## 学習者向けエラー診断・権限照会・FAST性能とJAR配布方針

種別：判断条件の記録と相談。reason名・API名・専用JARの採用は未決定。

### 1. エラーの原因を学習者が特定できるようにする

目標は「どのScratchブロックの、どの入力を、どう直せばよいか」が分かること。

調査した実装では、setBlocks の以下の原因が、同じ build_denied・詳細dataなしで返る。

- 許可された建築範囲の外
- player別の、1操作で置けるブロック数の上限超過

server側の処理量超過は work_limit_exceeded に分かれているが、要求量・上限を返していない。Scratch側も、大半のserverエラーをconsole警告へ流して後続処理を続けるため、画面上で原因を把握しにくい。

相談したい分類は次のとおり。名前は案。

| 原因 | reason案 | 伝えたい情報 |
| --- | --- | --- |
| 許可された建築範囲の外 | build_range_exceeded | 外れた座標、許可範囲 |
| player別の設置数上限超過 | block_count_limit_exceeded | 要求個数、適用中の上限 |
| server側の処理量上限超過 | 既存の work_limit_exceeded | 要求量、上限 |
| 座標の入力不正 | 既存の invalid_params を具体化 | 原因の入力欄・値・許容範囲 |

世界の高さ制約についても、事前判定と専用reasonを検討する余地がある。

次の対処が異なる原因はreasonを分け、入力箇所や値・上限はdataで伝える、という整理を相談したい。

ブロックID・状態名・状態値の間違いは既にreasonが分かれている。こちらは入力値や候補の表示を改善する。送信前のローカル検証にも、原因のproperty・値・候補を持たせる必要がある。

Scratchでは、発生元のブロック・スプライトとエラーを対応付け、原因と直し方を表示したい。新reasonの扱いは共有fixtureと各clientを合わせて検討する。protocolの版番号は今回決めない。

### 2. 適用中の権限・上限を照会できるようにする

McRemoteが使うLuckPermsの権限・メタは、認証済みhello時に一度取得し、接続へ保存する。各コマンドはその保存値を使い、変更は再接続で反映する。

内部ではオンライン／オフライン権限、建築範囲、設置数上限を保持しているが、helloは設置数上限 buildBlocks を返していない。

この接続に実際に適用中の権限・上限を返すAPIを検討したい。

- オンライン／オフライン権限
- 建築範囲
- 1操作の設置数上限
- server側の処理量上限（LP側の制限と区別）

helloにも同じ情報を含め、Scratchから値を読めれば、エラーになる前に調べられる。照会だけで接続の権限を更新せず、LPの最新設定も返す場合は適用中の値と分ける案。

### 3. FAST時の性能とJAR配布形態

- 懸念はFASTで大量のコマンドを流す時の性能。オンライン状態確認にMojang問い合わせがなくても、累積コストや寄与率は未計測。
- Paper／Javaの版による性能差次第で、統一JARの利便性より、分離・専用JARのリリースを優先する可能性を残す。
- 特定バージョンだけ専用JARを出し、ほかは共通JARを使う形も候補に含める。
- human ownerの「Paper 26は全体的に速くなった印象」は体感として保持し、比較計測や原因の特定とは分ける。
- 評価時はFASTのsetBlock連打とsetBlocks一括を分け、Paper／Java自体の差と、互換処理のコスト・専用化による改善余地を区別する。

DEBUG／TRACEは元々の診断用の役割として扱い、切替案内を新しい改善項目には数えない。FASTで個別のserverエラーが返らず、flushも個別エラーを集約しないことは既存の前提とする。
