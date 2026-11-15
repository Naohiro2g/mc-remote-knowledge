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

## 返却と照合（2026-11-15）

- McRemoteは、knowledge `b4b23631fc6f053fe4e228bb0447c9b4b9502901`を読み、PR #18に`expected_hello`を足した。返却票は
  McRemoteの`handoff-materials/2026-11-15-expected-hello/materials/RETURN_ja.md`（9,414 bytes、SHA-256
  `0ed6d29ae3c40fdeeac7e893a462159bc7326a850373e281491ef22990231ee8`）で、human ownerが会話で渡した
- coordinatorがGitHubのAPIで照合した。head `fbb9edc52cbe32634abf11a405204cc80a2a163d`。PR #19のmerge後のmain
  `3ccb3fd345faa228b195a15c3c45152f5dff7d04`からの差分は2 file（`RemoteSession.java` +4−4、`PreAuthTransportTest.java` +53）。
  CIのrun `43655720020`（headが同じ）は7 jobすべて成功。2026-11-15にhuman ownerがmergeした（merge commit
  `3126d3b946efe543be316427ae41eb5a7c1183b6`）。今のmainは`082df43145b4a5bfe5854a3985a82c936ed0ce76`（PR #20のmerge commit）
- 足したtest（`chat.post`と知らないmethodを、helloより前に送る2 case）は、直す前に2つとも、codeだけが違う理由
  （`-32600`と`-32000`）で落ちた。直した後、491 testが通った。mergeの後のmain（`082df43`）では、McRemoteの手元のbuildで
  539 testが通った（CIではない）
- 選んだcodeは`-32000`（`protocol_mismatch`、`auth_required`などと同じ）。`data.reason`、message、errorを返した後にflushして
  閉じること、helloの前に受けるmethodは変わっていない
- 3の一覧：wire「7.3 エラー設計」の表に無いreasonは12。うち9つは、wireの別の節か表の下の箇条で扱っている（`auth_required`、
  `method_not_found`、`out_of_bounds`、`pair_expired`、`pair_not_found`、`token_expired`、`token_invalid`、`token_not_found`、
  `token_revoked`）。wireに無いのは、`origin_not_set`（`-32000`。原点が要る操作で原点が無い）、`protocol_required`（`-32602`。
  helloの`protocol`が取れない）、`too_many_sessions`（`-32000`。束縛先の並行sessionの数が上限に達した）の3つ。表を直すときに
  一緒に扱う（hub NOTESの「学習者が直し方まで分かるエラー」の行）
- wireの`protocol_mismatch`と`expected_hello`の行と、Protocol InventoryのMcRemoteの列は、McRemote `2321.2.0`を出した後に
  直す（`00-hub/release-gate-notes_ja.md`の「2026-11-15 `2321.2`横断release gate」）
