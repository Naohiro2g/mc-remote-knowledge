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
