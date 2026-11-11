# F1の`protocol_mismatch`のcaseを決定に合わせる依頼（tooling）

> 多言語Client LibraryのE2の最初の判断として、helloの`protocol_mismatch`のerrorの形を`2026-11-10-01`で決めた。F1のfixture
> （minecraft-remote-tooling `8264c3881bb4128c14cda6d122641ebcfa67d9c5`、`00-hub/polyglot-f1-fixture-instructions_ja.md`）は、
> dataの欄の名前とcodeの番号を「未確定」としていた。この票は、F1をその決定に合わせる小さな依頼です。PythonとJavaは、
> 同じ時期にF3の票（`00-hub/polyglot-f3-instructions_ja.md`）で、F1のfixtureを各clientのtestへつなぐ。参照するknowledge commitは、
> この依頼が入ったmainのcommitです。

## 決まったこと（`2026-11-10-01`、wire「7.3 エラー設計」の`protocol_mismatch`の行）

- codeは`-32000`番台。McRemoteの`2321.1.0`は`-32600`を返していて、後で`-32000`番台へ移す
- `data`は`reason`（`protocol_mismatch`）、`server`（serverのprotocol）、`client_requires`（clientがhelloで申告したprotocol）
- clientは`data.reason`で判定し、codeでは分けない。McRemoteが移るまでの`-32600`も同じに扱う
- messageは英語の短文のまま

## 変えるもの

- `client-bootstrap-hello-v23.2.1.json`のF1-HE-09：peerのerrorの`data`に`server`と`client_requires`を足す（この例では
  `23.2.1`と`24.0.0`）。codeは範囲の代表の`-32000`のままでよい。`unresolved`から、dataの欄の名前の項を除く。messageの文言、
  codeの番号、切断の時機は、引き続きfixtureで決めない
- 同じfileに、caseを1つ足す：F1-HE-09と同じ対話で、errorのcodeが`-32600`で届く（McRemote `2321.1.0`までの形）。期待値は
  `protocol_mismatch`。clientがcodeで分けないことを確かめるcaseで、`-32600`を契約にするものではないと書く
- 値の形：McRemoteの公開のsource（`a38beaf121ce06594391237cb09745ec0da7649d`）で、`server`と`client_requires`の値がprotocolの
  文字列（例 `23.2.1`）であることを確かめる。文字列でなければ、fixtureを変える前に止めて、その形を返す
- `packages/protocol/README.md`の「`protocol_mismatch`の例はmessageに両方の版を示し、未確定の専用data field名を追加しません」
  を、決定に合わせて直す
- fixtureの`knowledge_contract.commit`は、この依頼が入ったknowledgeのcommitにする

## 進め方

- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。tag、Release、公開のworkflowの実行はしない
- ほかのcaseは変えない。直したいところが見つかったら、変えずに返す

## 返却

- PRの番号、merge commit、CIのrun ID
- 変えたfileの一覧（bytes、SHA-256）と、足したcaseのID
- McRemoteのsourceで確かめた値の形（file名とclass名）

## coordinatorがすること

- 返却をGitHubのAPI（PR、merge commit、CI、fileのbytes）で照合し、Protocol Inventoryの共有fixtureの列を直す
- merge commitを、F3の票のPythonとJavaへ伝える（同じPRか次のPRで、fixtureの取得元を固定し直してもらう）

## 返却と照合（2026-11-10）

tooling担当はknowledge `5e00768911feb7be1e54ae3b7e9c2d776b88927a`を読んだ。PR #5（head `b641e5d4914bc3a800580b8fa01eb950c0583c40`）を
merge commit `ea7838a78bf78947c7dde5876f6cc93b43f7e3cc`でmergeした（toolingの`main`の先頭）。PRのCIはrun 42783622850、merge後のCIは
run 42784120474で、どちらも成功した。coordinatorはGitHubのAPIで、PRとmerge、CIを確かめ、merge commitから4 fileを取ってbytesと
SHA-256を照合した（返却の値とすべて一致）。`8264c38`からの差分はこの4 fileだけ。

| file（`packages/protocol/`） | bytes | SHA-256 |
| --- | ---: | --- |
| `README.md` | 8,661 | `2cd1ee86cc50ec6204e543eba44efce2e1ae915596c8ca73d0611067e499c79d` |
| `test/client-bootstrap-owner-fixture.test.ts` | 5,461 | `e50296915d37ad5ecd74d821c0fcee768242e8454b68ac51139eed922c2d7072` |
| `test/fixtures/client-bootstrap-hello-v23.2.1.json` | 20,913 | `78297f05eb4352b0dabffab3242e933c1e68cb192bbb6d242019c7956c809d57` |
| `test/fixtures/client-bootstrap-v1.schema.json` | 9,953 | `e848bd3a61d4c0a737f7f3a8963baf2fcbb83247486f3d8aa69f022bb55a7ede` |

- F1-HE-09：errorの`data`は`reason`、`server`（`23.2.1`）、`client_requires`（`24.0.0`）で、codeは`-32000`
- F1-HE-10（新規）：同じ対話で、codeが`-32600`。期待値は`protocol_mismatch`。READMEに「後者を契約上のcodeとして採用しません」とある
- どちらも`unresolved`は、messageの文言、範囲の中のcodeの番号、切断の時機だけ。helloのfileは10 caseになり、F1は45 case
- 値の形：McRemoteの`RemoteSession`と`ProtocolInfo`で、2つの欄がprotocolの文字列であることを確かめた（担当の返却）
- schemaは、caseのfileごとに違う`knowledge_contract.commit`を受けられるように変えた。ほかの5本のfileは変わっていない
- 伝えること：Java担当から、F1-ER-01〜03の`matched_ids`は`[2]`でhelloのid 1を含まない（F1-FR-07はすべてを含む）ので、
  範囲をREADMEに書いてほしい、と返った（`00-hub/polyglot-f3-instructions_ja.md`の「返却と照合（2026-11-10）」）

## 追補の返却：`matched_ids`の範囲（2026-11-11）

tooling担当はknowledge `6f7ca001988387d172bd698579a0f42c72d24ac5`を読んだ。PR #6（head `c8b153eed1a7df5f955fcfc6c532a20faf610c5d`）を
merge commit `131f3153d7ab0b01b6e00a62a8249a55c8fc2ad0`でmergeした（toolingの`main`の先頭）。PRのCIはrun 42854773556、merge後のCIは
run 42855131443で、どちらも成功した。`ea7838a`からの差分は`packages/protocol/README.md`だけで、fixtureは変わっていない。coordinatorは
merge commitからfileを取り、9,383 bytes、SHA-256 `4a9d885b3a49c6cd572c666d1f83ee3936350239803756c0440e1e8659a7a69b`で返却と一致した。

- `matched_ids`は、そのcaseで検査するrequestに対応付けた応答idを、対応付けた順に並べる。前準備を含む対話全体の一覧ではない
- F1-ER-01〜03は`[2]`（helloのid 1は前準備）。F1-FR-07は相関そのものを検査するので`[2, 1]`、未知のid 99は`ignored_ids`
- 列に含めない前準備の応答も、clientは通常どおり処理する
