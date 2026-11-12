# F1の固定し直しと、E2の決定との違いを返す依頼（Python・Java・Scratch・TypeScript）

> 多言語Client LibraryのE2で、接続の振る舞いを`2026-11-11-01`①〜⑧と`2026-11-12-01`で決めた。toolingがF1をその決定に合わせ、
> minecraft-remote-tooling `36ebe9e63e4f0afcf949eae998832f68209b8119`（PR #7、48 case）で返した（照合は
> `00-hub/polyglot-f1-e2-fixture-instructions_ja.md`の「返却と照合（2026-11-11）」）。この票は、F1の取得元をそのcommitへ固定し直し、
> 各clientの今の振る舞いと決定との違いを返してもらう依頼です。human owner 2026-11-10：「クライアントの多言語化を最優先とする。
> その先のUnity版マイクラリモコンを急ぐため」。参照するknowledge commitは、この依頼が入ったmainのcommitです。各担当は
> 「共通」と、自分の節を読んでください。

## 共通

### 決まったこと

- `2026-11-11-01`（wire「3.4 id 規律」「6.5 認証：ペアリングフロー」）
  - ①承認を拒む専用の応答は今は持たない。承認されなければ`pair_expired`になる
  - ②接続が閉じたら（相手のEOF、socketのerror、自分で閉じたとき。timeoutで回収したときを含む）、応答待ちのrequestを
    すべて、localな「完了不明」の失敗にする。serverのerrorとしては扱わず、reasonを作らない。LFの無い末尾は応答にしない。
    例外の型は言語ごと
  - ③応答は既定で長く待つ。その接続で最後に受信してからの時間で見て、超えたら「完了不明」で接続を回収する。生存確認は
    別に持つ。値と設定の仕方は言語ごと
  - ④自動で再送しない
  - ⑤接続が切れた後の次の呼び出しで、自動でつなぎ直す（既定で有効）。条件はDECISIONSの⑤のA〜G（「未送信」と
    「完了不明」を分ける、FASTとflushの境界、版と`catalogHash`の照合をやり直す、pairingは自動で進めない、一回に
    まとめる、backoffのばらつき、生存確認で切れたと分かる）。helloの`build`で、最後に成功を確かめたdimensionとoriginを戻す
  - ⑥serverが不正な行にerrorを返すかは契約にしない
  - ⑦認証reason（`token_expired`、`token_revoked`、`token_not_found`、`token_invalid`）でtokenを捨てたら、tokenなしのhelloへ
    戻り、`auth_required`のときだけpairingに入る。pairingは一接続試行につき一度（`2026-08-30-03`）
  - ⑧clientが`expires_in`を過ぎたと判断したpairingの期限切れは、`pair_expired`と同じ意味で扱い、serverのerrorの形（code
    とreason）は作らない。serverが言ったのか、clientが判断したのかが分かるようにする
- `2026-11-12-01`（wire「6.2 応答 `result`」）：clientが、成功したhelloの応答の版を互換でないと判定したら、次のrequestを
  送らずに接続を閉じ、applicationへ失敗を返す

### F1の取得元

- tooling `36ebe9e`の`packages/protocol/test/fixtures/`の、F1の6本（`client-bootstrap-{framing,hello,pairing,blocks,errors,close}-v23.2.1.json`、
  48 case）、`client-bootstrap-v1.schema.json`、`block-value-v22.json`（blocksの`value_refs`の範囲）。形の説明は同じcommitの
  `packages/protocol/README.md`
- `131f315`から変わったのは、close（F1-CL-03、05に`local_failures`と`pending_ids`）、pairing（F1-AU-07の前提、F1-AU-08〜10を
  追加。`pairing_attempts`）、schemaの3 file。ほかのfileとLICENSE（1,070 bytes、SHA-256
  `aa329a0bafc839b95124306141db13a381de45818bf629e983c44ea55ab5a7fb`）は同じbytes
- copyで持つときは、fileごとのbytesとSHA-256をtestで確かめる（F2、`2026-10-22-07`）

### すること

1. 取得元を`36ebe9e`へ固定し直し、CIでF1の48 caseをすべて通す。skipを残したら済みにしない
2. ②④⑦⑧と`2026-11-12-01`のそれぞれについて、今の振る舞いと決定との違いを表にする。違うものは直す。直すときは、そのcase
   （F1に無ければ担当のunit test）が、直す前に意図した理由で落ちることを見てから直す
3. ③⑤：今の振る舞い（timeout、生存確認、つなぎ直し）を書き、決定のとおりに入れるためのAPIの形（timeoutの設定、つなぎ
   直しの有効と無効、つなぎ直したことの知らせ、「未送信」と「完了不明」の失敗の型）を案にして返す。入れるのは次の票
   （TypeScriptは下の節のとおり、この票で入れる）。F1の③⑤のcaseは、toolingに頼んでいる
   （`00-hub/polyglot-f1-e2-ops-fixture-instructions_ja.md`）
4. caseが契約と違う、または読み方が決まらないと思ったら、そのcaseのIDと理由を返す。決まっていないことは、clientで新しく
   決めない
5. 認証の流れを変えたら、実McRemoteとのpulse（hello → `world.setBlock` → `world.getBlock`）を1本通す。相手は担当の手元の
   Paperと、公開のMcRemote `2321.1.0`（`protocol_mismatch`はcode `-32600`で届くが、reasonで判定するので通る）。Minecraftの中
   での承認など、人の操作が要るなら、その前で止めて手順を返す（human ownerが行う）。「live-auto相当」で、scriptとPASSの
   summaryを残す
6. 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい（権限で拒まれたら、human ownerが行う）。tag、Release、
   公開のworkflowの実行はしない
- token、`pairing_id`、private endpoint、host、IP、player名、座標を、返却と公開のartifactへ書かない

## Python

- `2026-11-12-01`：応答の版の不一致は、F3で`Minecraft.create()`の失敗にした。接続を閉じているかを確かめる
- ⑦：認証reasonの後の流れが、F1-AU-08〜10のとおりかを確かめる

## Java

- ⑦：TypeScriptの返却（2026-11-11）で、Javaは認証reasonでtokenを捨てた後、すぐpairingへ進むと見えた。tokenなしのhelloへ
  戻す（F1-AU-08〜10）
- ⑧：Javaは、clientが判断したpairingの期限切れを、serverのerrorと同じ形（`-32000`、`pair_expired`）で作ると見えた。serverの
  errorの形を作らずに、同じ意味で扱い、どちらが判断したかが分かるようにする
- 既定の申告protocolは`23.0.0`のまま（human owner「24.0.0で揃えば問題ない」）。F1のcaseは`23.2.1`の申告を使ってよい

## Scratch

- Scratchは、F1をtestにつないでいない（Protocol Inventoryの「共有fixtureの使い方」）。1は、F1をtestにつなぐかを案にして
  返す（つなぐなら、どの層で、何caseか。F1は直接のTCPが基準で、browserのWebSocketの境界とは分ける）
- 2は、blockやUIの振る舞いを変えずに直せるものを直す。block、ペアリングのhat、表示を変えるものは、直さずに案を返す
  （human ownerが決める）

## TypeScript

- `2026-11-12-01`、②⑦⑧は、最初の縦sliceで今の形のまま合っている（照合は`00-hub/polyglot-typescript-start-instructions_ja.md`の
  「返却と照合（2026-11-11）」）。1で`36ebe9e`へ固定し直す
- ③⑤を、この票で決定のとおりに入れる。APIの形は担当が案にして返す。F1の③⑤のcaseが届くまでは、担当のunit testで持つ。
  toolingのcaseが届いたら、coordinatorが伝えるので、取得元を固定し直す
- ⑤のpairingは自動で進めない（D）。`onPairing`を渡していても、つなぎ直しで`auth_required`になったら止めて知らせる

## 返却

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- fixtureの取得元の前と後（commit、copyならfileごとのbytesとSHA-256）と、fileごとのcase数とPASS数
- 2の表（決定ごとに、前の振る舞い、決定との違い、直したか、直したなら落ちたcaseと前と後）
- 3：今の振る舞いと、APIの形の案（TypeScriptは、入れた形とtest）
- pulse（したなら）：日付、Paperの版、McRemoteの版、手順、結果、認証の方法、片付けの方法
- 違うと思ったcase、決めずに残したこと
- Protocol Inventoryの「共有fixtureの使い方」の自分の行の、前と後
- Scratchだけ：F1をtestにつなぐかの案。直さなかったblockやUIの振る舞いの案

## coordinatorがすること

- 返却を、GitHubのAPI（PR、merge commit、CI、fixtureのbytes）で照合し、Protocol Inventoryへ写す
- 3の案を突き合わせ、③⑤を入れる票を作る
- toolingの③⑤のcaseのmerge commitを伝える

## 返却と照合（2026-11-12）

4つの担当とも、knowledge `076a127a22eaf0188c1d13822bfd55bfeee9ec38`を読んだ（この票が入った`0b41bfd`を含み、この票の本文は今と
同じ）。coordinatorはGitHubのAPIで、PR、merge commit、CI、fixtureのcopyまたはlockのbytesを確かめた。

| client | PRとmerge commit | CI | F1の取得元とPASS | 直したもの |
| --- | --- | --- | --- | --- |
| Python | #15 → `9e64b492a90c967675477a495287d9080428b390` | PR `43071491555`、merge後`43071750399` | `36ebe9e`、48/48 | ②⑦⑧、`2026-11-12-01` |
| Java | #4 → `223ef287f1cb17a7b2cdbf619d08d0ffd7a17e37` | head `43157405386`、merge後`43157617686` | `36ebe9e`、48/48 | ⑦⑧ |
| Scratch | #33 → `d9a7ec6e825d1a5602db57577009c28830ad0016` | head `43092698764`（push） | `36ebe9e`をlockに固定。再生は0 | ②の一部、`2026-11-12-01` |
| TypeScript | #3 → `2b59c5a6e6f2401148f4c79af108b7a6b1f9aba2`、#4 → `f8af802a813c81ad99631e5eb5454de04ae8ae2e` | #3：PR `43070666366`、merge後`43156347232`。#4：PR `43160255273`、merge後`43165316133` | `0d120e5`、v1 52/52、v2 9/12 | ②の型、⑦⑧、③⑤を入れた |

### Python

- PR #15（head `0f4ee86117971643c0e26f6060f3c92e5de09216`、base `8cb2d55db4ee2c59bee3fca2957354aed60ad126`、16 file）。CIは2 runとも
  成功。copyした9 fileは、tooling `36ebe9e`とGit blobで一致した。全846 testが通った（件数は担当の返却による）
- ②：EOFでは例外を返していたが、応答待ちの一覧を持たず、送った後の完了不明を分けていなかった。自分で閉じる時は、応答待ちの
  workerの終わりを待っていた。応答待ちをすべて解決し、`ConnectionLostError`に`completion_unknown`（送り始めた後はtrue、未送信は
  false）を付けた。F1-CL-03、05が、直す前に意図した理由で落ちた
- ⑦：tokenを捨てた後、すぐpairingしていた。直す前にF1-AU-08〜10が落ちた
- ⑧：clientが判断した期限切れで、serverに似せた`McRpcError(-32000, reason=pair_expired)`を作っていた。`PairingExpiredError`
  （`origin="client"`、codeとreasonを持たない）に分けた
- `2026-11-12-01`：`create()`は後始末していたが、`hello()`を直接呼ぶと、不一致の後も接続が残っていた
- ④：違いは無かった
- ③⑤の今：応答の待ちはsocketのtimeoutで60秒。超えると接続を回収する。呼び出しごとの設定と、最後の受信から数えるtimerは無い。
  生存確認とつなぎ直しは無い。案：`ConnectionOptions`、`LivenessOptions`、`ReconnectOptions(enabled)`、`on_reconnect(ReconnectInfo)`、
  `call_options`、`RequestNotSentError`と`CompletionUnknownError`（どちらも`ConnectionLostError`の子）
- pulse：2026-11-12、Paper 1.21.11（build 132）、McRemote `2321.1.0`でPASS。置いたブロックは元に戻した
- 違うと思ったcase：無し（AU-07の一回だけのsnapshotと、AU-08〜10の回復の流れを分けて読んだ）

### Java

- PR #4（head `427581a5ad5d13e0a05103607775e80e585f2c19`、base `dc8992324122611a579f66219a43c88d480fa844`、15 file）。自動で起きた
  pushとPRのrun（`43098178267`、`43098202456`）はjobが0本のqueuedで止まり、cancelもrerunもできなかったので、担当が同じheadで
  workflow_dispatchし直した（`43157405386`、build (21)とbuild (25)が成功）。merge後のrun `43157617686`も成功。copyした13 fileは、
  tooling `36ebe9e`とGit blobで一致した。返却の資料は同じcommitの`docs/polyglot-f1-e2_ja.md`
- ⑦：tokenを捨てると、すぐpairingへ進んでいた。`pairingListener`が無ければ`PairingRequiredException(token_*)`だった。直す前に
  F1-AU-08〜10が落ちた。今は、`pairingListener`が無くても、認証を強制しないserverにはそのままつながる
- ⑧：clientが判断した期限切れで、`RemoteCallException(-32000, ..., {reason: pair_expired})`を作っていた。`PairingExpiredException`
  （codeとdataを持たない）に分けた。担当のunit testが、直す前に落ちた
- ②、④、`2026-11-12-01`：違いは無かった。`2026-11-12-01`は担当のunit testを足した（足した時から通った）
- ③⑤の今：`readTimeout`が既定10秒。超えると、そのidだけを失敗にして接続を使い続ける。これは③の却下案「timeoutの後も接続を
  使い続ける」に当たる。生存確認とつなぎ直しは無い。案：`Builder.responseTimeout`、TCPのkeepalive、`Builder.autoReconnect`（既定
  true）、`reconnectListener`、`CompletionUnknownException`と`NotSentException`（どちらも`TransportException`の子）
- pulse：2026-11-12、手元のPaperとMcRemote（helloで`23.2.1`、Minecraft 1.21.11）でPASS。⑦の流れは、pairingに入ったことからの推定で、
  wireでは観測していない（F1-AU-08〜10で確かめている）
- 違うと思ったcase：無し。F1-AU-07の観測の終わりをREADMEに書いてほしい

### Scratch

- PR #33（head `483087d8b79fbb52515ad07701e9046ffcc74c1b`、base `dc2840ba3c5c9d6938555ed737bc199acca2586e`、6 file）。PRのrun
  `43092902585`は、scratch-vmのjobがin_progressのまま止まり、のちにcancelされた。担当は、同じheadのpushのrun `43092698764`
  （10 jobすべて成功）を根拠にmergeした。merge commitの木はheadと同じ。merge後のrun `43097182559`は、照合した時点でqueuedのまま
  だった。変えた6 fileのbytesとSHA-256は返却どおり
- 固定し直し：lockの取得元を`36ebe9e`にし、F1の6本とschemaを足した。9 fileのSHA-256はtoolingと一致した。F1の対話はtestで
  再生していないので、PASSは0件（schemaと件数の検査だけ）
- ②：socketのerrorで、応答待ちを回収して閉じるようにした。閉じた時のcodeとreasonが、応答待ちの失敗にも一緒に渡る点は、表示を
  変えずには分けられないので、案で返した。LFの無い末尾は、VMにTCPの区切りが無いので、Bridgeと分担する案
- `2026-11-12-01`：互換でないと判定したら、自分で閉じるようにした
- ④：違いは無かった
- 直さずに案で返したもの（blockやUIが変わるので、この票の「Scratch」の節のとおり）：⑦（今はtokenを捨てた後、すぐpairingへ進む）、
  ⑧（pollの前に期限を調べない。どちらが判断したかの案内が無い）
- ③⑤の今：通常のrequestの応答のtimeoutは無い。生存確認とつなぎ直しは無い。closeでbuild contextを消す。案は内部のconnection
  policy（`requestIdleTimeoutMs`、`autoReconnect`）と、成功を確かめたdimensionとoriginの保存
- F1をつなぐ案：VMのFakeWebSocketで41 case相当（FR-07、hello 10、pairing 10、blocks 12、errors 3、close 5）、TCPに固有の
  7 case（FR-01〜06、CL-03）はBridgeとtoolingのTCPの側。41 caseは直接のTCPの対話をそのまま再生したPASSではないので、数え方を
  coordinatorと合わせたい
- pulse：認証の流れを変えていないので、していない

### TypeScript

- PR #3（head `2b4201e7dff993de508092840254823315448d71`）と#4（head `0cadc03490240382652b56d0a897cb8b14ea8f19`）を、human ownerが
  mergeした（agentのmergeはClaude Codeの権限で拒否された）。CIの6 runはすべて成功。#4のmerge後の`test/fixtures/protocol/`の
  11 fileは、tooling `0d120e5`とGit blobで一致した
- 取得元：#3で`36ebe9e`へ、#4で`0d120e5`へ固定した（toolingの票の2のmerge commit）。v1は52 caseすべてPASS。v2は12 caseのうち
  9 caseがPASSで、OP-06（FASTとflushが無い）、OP-08（下の指摘）、OP-11（handle、cursor、catalogのcacheが無い）はtodoとし、
  合格に数えていない
- ⑦：`onPairing`を渡さないと、tokenを捨てた後に、tokenなしのhelloへ戻らずに止まっていた。直す前にF1-AU-09が落ちた
- ⑧：pollの順を「すぐpoll→間隔を待つ→期限を見る→poll」に変えた。前の順では、期限を過ぎた後に1回pollを送り、serverに期限切れを
  言わせうる
- ②：意味は合っていた。型を`CompletionUnknownError`と`NotSentError`に分けた
- ④、`2026-11-12-01`：違いは無かった
- ③⑤（入れた）：`ConnectOptions`の`responseTimeout`（仮の既定15分。最後の受信から数え、呼び出しごとに延ばせる）、`keepAliveDelay`
  （仮の既定30秒、TCPのkeepalive）、`reconnect`（既定で有効。仮の間隔は500msから30秒、諦めるまで5分）、`onReconnect`
  （`ReconnectEvent`：前と後のhello、serverとsessionと`catalogHash`が変わったか）。つなぎ直しで`auth_required`なら、pairingせずに
  `NotSentError`で止める。つなぎ直しで戻すbuildは、`call()`で成功した`build.setDimension`と`build.setOrigin`だけを追う。値は実測で
  決める。⑤Gは、OSのTCP keepaliveに任せている
- pulse：2026-11-12、手元のPaper 1.21.11とMcRemote `2321.1.0`で、#3と#4のheadでそれぞれPASS（`minecraft:gold_block`）。どちらも
  元へ戻した
- 違うと思ったcase：F1-AU-07の観測の終わり、F1-OP-08のpairingの接続、v2の`expected`の読み方、F1-OP-05の`connect_error terminal`の
  表し方（待ち方と回数は確かめていない）

### 前の照合の訂正

- この票の「TypeScript」の節は、TypeScriptの⑦が最初の縦sliceで合っているとした（`00-hub/polyglot-typescript-start-instructions_ja.md`
  の「返却と照合（2026-11-11）」による）。実際は、`onPairing`を渡さないときに違いがあった。F1-AU-08〜10は、2026-11-11の45 caseに
  無かった。今はPR #3で直っている

### 次にすること

- ③⑤を入れる票（Python、Java、Scratch、C#）：各clientの案は上のとおり。TypeScriptの形を参考に並べる
- Scratchの⑦と、F1をtestにつなぐ案は、human ownerが決める
- F1のcaseへの指摘は、`00-hub/polyglot-f1-e2-ops-fixture-instructions_ja.md`の「返却と照合（2026-11-12）」にまとめた
- どれもhub NOTES 2026-11-12の「多言語Client LibraryのE2を各clientへ入れる」の行
