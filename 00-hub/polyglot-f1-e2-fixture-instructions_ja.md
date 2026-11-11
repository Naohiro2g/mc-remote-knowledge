# F1のcaseをE2の決定に合わせる依頼（tooling）

> 多言語Client LibraryのE2で、F1が「未確定」としていたことを`2026-11-11-01`で決めた（案は
> `10-protocol/polyglot-e2-plan_ja.md`のU1〜U6。⑦⑧はTypeScriptの返却で見えたJavaとの違い）。新しいwireは足していない。この票は、
> F1のfixture（minecraft-remote-tooling `131f3153d7ab0b01b6e00a62a8249a55c8fc2ad0`）を、その決定に合わせ、F1に無い流れを足す
> 依頼です。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 決まったこと（`2026-11-11-01`、wire「3.4 id 規律」「6.5」）

- ①承認を拒む専用の応答は今は持たない。承認されなければ`pair_expired`になる
- ②接続が閉じたら（相手のEOF、socketのerror、自分で閉じたとき。timeoutで回収したときを含む）、clientは応答待ちのrequestを
  すべて、localな「完了不明」の失敗にする。serverのerrorとしては扱わず、reasonを作らない。LFの無い末尾は、JSONとして
  閉じていても応答にしない。例外の型は言語ごとに決める
- ③応答は既定で長く待つ。その接続で最後に受信してからの時間で見て、超えたら「完了不明」で接続を回収する。生存確認は別に持つ。
  値と設定の仕方は言語ごと
- ④自動で再送しない
- ⑤接続が切れた後の次の呼び出しで、自動でつなぎ直す（既定で有効）。新しい接続のhelloで、最後に成功を確かめたdimensionと
  originを`build`で戻す。つなぎ直せなかった呼び出しは「未送信」として「完了不明」と分ける。前の接続で送ったFASTの設置を、
  つなぎ直した後の`connection.flush`が保証するように見せない。版の互換判定と`catalogHash`の照合をやり直す。pairingが要る
  ときは自動で進めない（条件の全体はDECISIONSの⑤のA〜G）
- ⑥serverが不正な行にerrorを返すかは契約にしない
- ⑦認証reasonでtokenを捨てたら、tokenなしのhelloへ戻り、`auth_required`のときだけpairingに入る（wire「6.5」のとおり）
- ⑧clientが判断したpairingの期限切れは、`pair_expired`と同じ意味で扱い、serverのerrorの形は作らない。どちらが判断したかが
  分かるようにする

## 変えるもの

- F1-CL-03（行の途中でEOF）とF1-CL-05（応答待ちのrequestを残してEOF）：`expected`で、id 2が②の「完了不明」の失敗として
  終わることを表す。例外の型は言語ごとなので、fixtureでは決めない。`unresolved`から、決まった項（末尾の扱い、応答待ちの
  解決の仕方、自動の再送）を除く
- F1-AU-07：`unresolved`の「承認を拒む専用message／pair_denied reasonは契約に無い」を、①で決まったこととして書き直す
- `basis`に`00-hub/DECISIONS_ja.md`の`2026-11-11-01`を足す（schemaが受けられる形で）
- expectedの欄の名前と形（たとえば新しい欄を足すか、今の`unanswered_ids`の意味を書き足すか）は、toolingが選び、理由を返す
- ⑦のcaseを足す：保存したtokenのhelloが認証reason（たとえば`token_expired`）で拒まれ、tokenを捨ててtokenなしのhelloを送る。
  `auth_required`が返ったらpairingへ進む。認証を強制しないserverの形（tokenなしのhelloがそのまま通り、pairingしない）も
  入れる。今のF1には、この流れが無い（TypeScriptの返却）
- pairingの後のhelloが、また認証reasonで拒まれる流れのcaseを足す。一接続試行につき一度だけpairingする（`2026-08-30-03`）ので、
  2回目のpairingへ進まずにapplicationへ失敗を返す
- 次のcaseを足すかは、案を返す。値は言語ごとなので、timeoutの値をfixtureで決めない
  - ③のtimeoutと、④の再送しないこと
  - ⑤のつなぎ直し：切断の後の次の呼び出しで、新しい接続のhelloに`build`が戻ること。つなぎ直せなかった呼び出しが「未送信」に
    なること。FASTのnotificationを送った後に切れ、つなぎ直した後の`connection.flush`が、前の接続の設置を保証しないと分かること。
    つなぎ直したhelloで版が合わないとき失敗すること。stepsとexpectedで表せるか、表せないなら何が足りないかも返す
  - ⑧：clientが`expires_in`を過ぎたと判断して止めるcase。F1-AU-02は、期限の後にpollを1回送る前提になっている
    （TypeScriptの返却）
  - clientの側の互換判定で不一致になった後に、接続を閉じること（TypeScriptの返却）。閉じることが契約から読めるかも返す
- `packages/protocol/README.md`の、closeとEOFの説明を決定に合わせる
- 変えたcaseのfileの`knowledge_contract.commit`は、この依頼が入ったknowledgeのcommitにする

## 進め方

- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。tag、Release、公開のworkflowの実行はしない
- ほかのcaseは変えない。直したいところが見つかったら、変えずに返す

## 返却

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- 変えたfileの一覧（bytes、SHA-256）と、変えたcaseのID、caseの数
- expectedの形を選んだ理由
- 足したcaseのIDと、案を返したcase（③④⑤⑧、互換判定の後のclose）について、足したか、足さなかったかと、その理由

## coordinatorがすること

- 返却をGitHubのAPI（PR、merge commit、CI、fileのbytes）で照合し、Protocol Inventoryの共有fixtureの行を直す
- merge commitを、TypeScriptの担当へ伝える。PythonとJavaとScratchへは、固定し直しと、決まったこととの違いを返してもらう票を作る

## 返却と照合（2026-11-11）

tooling担当はknowledge `562b5c008c7a4e391f04a79ed4496bbd44670896`を読んだ（この票の本文は今と同じ）。minecraft-remote-tooling PR #7
（head `992d4180775c67abb6baf57fb1c5d25bbc8764a6`、base `131f3153d7ab0b01b6e00a62a8249a55c8fc2ad0`）を、担当が2026-11-11にmerge
commit `36ebe9e63e4f0afcf949eae998832f68209b8119`でmergeした（`main`の先頭）。coordinatorはGitHubのAPIで、PR、merge commitの親、
CI（PRのrun `42999179142`、merge後のrun `42999520995`、どちらも成功）、変わった6 fileのbytesとSHA-256を確かめた。

| file（`packages/protocol/`の下） | bytes | SHA-256 |
| --- | ---: | --- |
| `F1_E2_PROPOSALS_ja.md` | 9,672 | `aa574639604d2ed36a1947dbab6e566239451b2f46074000d426b5540206d49a` |
| `README.md` | 11,955 | `ddb8e23d1e5f4424a6788a11d24bedc115c2a5330957898eb388f3e33ca9fd62` |
| `test/client-bootstrap-owner-fixture.test.ts` | 7,925 | `bd9abfff02deffbb14dd3dba1936ddb516b2623a91ce65074c5cf928220c0594` |
| `test/fixtures/client-bootstrap-close-v23.2.1.json` | 14,884 | `a030cc72aa0e4f41575cb15610b1e06e941d3eab07157ce47f0eafe744475154` |
| `test/fixtures/client-bootstrap-pairing-v23.2.1.json` | 35,577 | `5864c23ef3f31af6134d36770cab80b569b708b35fd3fdbed69fb6db195e3aeb` |
| `test/fixtures/client-bootstrap-v1.schema.json` | 10,916 | `8c3e4ff6e7b5b0cf438d358578096579dafab699a40df9cd56de7b9513837413` |

- case：F1は48 case（closeが6、pairingが10。framing、hello、blocks、errorsは変わらない）。変えたのはF1-CL-03、F1-CL-05、
  F1-AU-07。足したのはF1-AU-08〜10。ほかの42 caseと、変えていない15 fileは前と同じ。変えた2 fileの`knowledge_contract.commit`は
  `562b5c0`
- expectedの形：CL-03とCL-05は、`unanswered_ids: [2]`を残し、`local_failures: [{ id: 2, outcome: "completion_unknown" }]`と
  `pending_ids: []`を足した。「応答が無い」という観測と、「clientが完了不明として失敗を返した」結果を分けるため。
  `unanswered_ids`の意味だけを変えると、今のconsumerの未応答の検査を、失敗まで確かめたものと読み違えうる。`local_failures`は
  wireではなく期待値のmetadataで、schemaは`id`と`outcome`だけを許し、serverのcodeとreasonを入れない。例外の型、名前、message
  は求めない
- AU-07：承認を拒む専用の応答が無いことを、`unresolved`から、①に従うpeerの前提へ移した
- 足したcase：AU-08（認証reasonでtokenを捨て、tokenなしのhello、`auth_required`、pairing、helloが成功）、AU-09（tokenなしの
  helloが通り、pairingしない）、AU-10（pairingの後のhelloがまた認証reasonで拒まれ、2回目のpairingをせずにapplicationへ失敗を
  返す）。`pairing_attempts`で、接続試行の全体での`auth.pairBegin`の回数を表す（TCPの張り直しを2回目のpairingの許可と取り違え
  ないため）。`discard_token`は拒まれたtokenを捨てることで、AU-08では新しく取ったtokenと両立する
- 案で返したもの（fixtureには足していない）：③④⑤⑧と、互換判定の後のclose（`F1_E2_PROPOSALS_ja.md`の「追加案の返却」）。
  今の`steps`と`expected`では、applicationの呼び出しとその結果、clientの設定に結びつく仮想の時計、「送らないこと」を見る
  区間、notification、接続ごとの観測、request idの無いlocalな終了が表せない。互換判定の後のcloseは、clientが閉じることと
  その時機が契約に書かれていないので、足す前にcoordinatorへ確かめるとした。ほかに、JSONは閉じているがLFの無い末尾でのEOF、
  socketのerrorと自分で閉じた時の応答待ちの回収も、今のcaseでは直接確かめていない
- 返却の後に決まったこと：互換判定の後のcloseは`2026-11-12-01`で決めた。案で返したものは、toolingへの次の票
  （`00-hub/polyglot-f1-e2-ops-fixture-instructions_ja.md`）で頼む
