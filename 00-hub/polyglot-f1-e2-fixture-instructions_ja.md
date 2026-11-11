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
