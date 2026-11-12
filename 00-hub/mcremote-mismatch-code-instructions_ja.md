# protocol_mismatchのcodeを-32000番台へ移す依頼（McRemote）

> `2026-11-10-01`①で、helloの`protocol_mismatch`のcodeを`-32000`番台と決めた（wire「6.3 失敗」「7.3 エラー設計」）。出荷済みの
> `2321.1.0`は`-32600`（JSON-RPCのInvalid Request）を返す。human owner 2026-11-12：「codeの移しかえを次の票にして、同じreleaseに
> 入れる」。同じreleaseには、credentialのfileの権限（`2026-11-11-03`、PR #16）と、ゲーム内の文の言語（`2026-11-12-02`、PR #17）が
> 入る（hub NOTES 2026-11-12の「McRemoteの次のrelease」の行）。参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 欲しいもの

- helloの`protocol_mismatch`を、`-32000`番台のcodeで返す。番号は、ほかのreasonと同じく、範囲の中でMcRemoteが選ぶ
- 変えないもの：`data`の`reason`（`protocol_mismatch`）、`server`、`client_requires`。messageの英語の短文。errorを返した後に
  閉じること。互換判定（majorの一致、serverのminorが同じか上、patchは見ない）

## すること

1. 先にtestを直し、今の`-32600`で落ちることを確かめる（落ちたlogを返却に残す）
2. 直す。選んだcodeと、その理由（ほかのreasonのcodeとの関係）を返却に書く
3. ほかにも、形の正しいrequestへ`-32600`を返すreasonがあれば、変えずに一覧を返す
4. 既定のbranchへのPRにする。localとCIの検査を通す。mergeはhuman ownerが判断する。tag、Release、公開のworkflowの実行は
   しない。releaseの版と時期は、human ownerが決める

clientは`data.reason`で判定し、codeでは分けない（`2026-11-10-01`③）。共有fixtureには、`-32000`のF1-HE-09と、出荷済みの
serverのための`-32600`のF1-HE-10がある。どちらもこのままにする。

## 返却

- 実際に読んだknowledge commit
- 1で落ちたtestと、そのlogの抜粋
- 選んだcodeと理由
- 3の一覧（あれば）
- PRの番号とhead、CIのrun ID

## coordinatorがすること

- PRの差分、test、CIをGitHubのAPIで照合する
- wire「7.3 エラー設計」の`protocol_mismatch`の行と、Protocol InventoryのMcRemoteの列を、mergeの後に直す
- human ownerにreleaseの時期を聞き、台帳`00-hub/release-train-notes_ja.md`に行を足す

## 返却と照合（2026-11-12）

- McRemoteは、knowledge `076a127a22eaf0188c1d13822bfd55bfeee9ec38`を読み、PR #18を返した（まだmergeしていない）。head
  `2ac8dd3a6e81c8fafc8d7458c79a9f2c776606a7`、baseは`main`の`cdafcfd804614def19a35b099bedc93697ca4899`。CIのrun `43068805626`
  （`workflow_dispatch`、headが同じ）は7 jobすべて成功
- 差分は2 file。`RemoteSession.java`は、`protocol_mismatch`のcodeを`-32600`から`-32000`へ変えた（`auth_required`、
  `permission_denied`などと同じcode）。`PreAuthTransportTest.java`に3 case（clientの申告`22.0.0`、`24.0.0`、`23.3.0`、serverは
  `23.2.1`）を足した。3 caseは、直す前に、codeだけが違う理由で落ちた。直した後、441 testが通った
- `data`（`reason`、`server`、`client_requires`）、message、errorの後に閉じること、互換判定は変わっていない。F1-HE-09、10も
  変わっていない
- 3の一覧は`expected_hello`の1件だった。helloが成功する前に`auth.*`以外のmethodが来ると、code `-32600`のerrorを返して閉じる。
  このreasonはwire「7.3 エラー設計」に無かった。`2026-11-12-03`で契約に入れ、下の「追加の依頼：expected_hello」で、PR #18に
  足してもらう。PR #18のmergeは、足した後にする

## 追加の依頼：expected_hello（2026-11-12）

> 返却の3で、`expected_hello`が契約に無く、codeが`-32600`だと分かった。`2026-11-12-03`で、wire「7.3 エラー設計」に`-32000`番台の
> reasonとして入れた。human owner 2026-11-12：「expected_helloもPR #18に足してもらう票を起案して」。参照するknowledge commitは、
> この追加が入ったmainのcommitです。

### 欲しいもの

- `expected_hello`を、`-32000`番台のcodeで返す。番号は、ほかのreasonと同じく、範囲の中でMcRemoteが選ぶ
- 変えないもの：`data`の`reason`（`expected_hello`）、message、errorを返した後に閉じること、helloの前に受けるmethod
  （`hello`と`auth.*`）

### すること

1. 先にtestを足し、今の`-32600`で落ちることを確かめる（落ちたlogを返却に残す）
2. 直して、PR #18の同じbranchに足す。PRの説明と注記も合わせる
3. McRemoteが返すreasonのうち、wire「7.3 エラー設計」の表に無いものがあれば、変えずに一覧を返す（reason、code、どんなときに
   返すか）
4. localとCIの検査を通す。mergeはhuman ownerが判断する。tag、Release、公開のworkflowの実行はしない

### 返却

- 実際に読んだknowledge commit
- 1で落ちたtestと、そのlogの抜粋
- 選んだcodeと理由
- 3の一覧（あれば）
- PR #18の新しいhead、CIのrun ID

### coordinatorがすること

- 足した差分、test、CIをGitHubのAPIで照合する
- mergeの後、wire「7.3 エラー設計」の`protocol_mismatch`と`expected_hello`の行（「McRemote `2321.1.0`まではcode `-32600`」）と、
  Protocol InventoryのMcRemoteの列を直す
- human ownerにreleaseの時期を聞き、台帳`00-hub/release-train-notes_ja.md`に行を足す
