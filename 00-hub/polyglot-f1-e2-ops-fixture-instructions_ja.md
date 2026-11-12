# F1に、待ち方、つなぎ直し、clientが判断する終わりのcaseを足す依頼（tooling）

> F1をE2の決定（`2026-11-11-01`）に合わせる票（`00-hub/polyglot-f1-e2-fixture-instructions_ja.md`）で、toolingは48 caseを返し
> （minecraft-remote-tooling `36ebe9e63e4f0afcf949eae998832f68209b8119`）、③④⑤⑧と互換判定の後のcloseは、今の`steps`と`expected`
> では表せないとして案を返した（同じcommitの`packages/protocol/F1_E2_PROPOSALS_ja.md`）。互換判定の後のcloseは`2026-11-12-01`で
> 決めた。この票は、その案を形にして、caseを足す依頼です。TypeScriptが③⑤を入れ、C#が最初の縦sliceを作るときに使う。
> 参照するknowledge commitは、この依頼が入ったmainのcommitです。

## 決まったこと

- `2026-11-12-01`（wire「6.2 応答 `result`」、versioning「8.3 不一致時」）：clientが、成功したhelloの応答の版を互換でないと
  判定したら、次のrequestを送らずに接続を閉じ、applicationへ失敗を返す
- `2026-11-11-01`の②（閉じたら応答待ちをすべてlocalな「完了不明」の失敗にする。相手のEOF、socketのerror、自分で閉じた
  とき、timeoutで回収したときを含む）、③（最後に受信してからの時間で見る。生存確認は別）、④（自動で再送しない）、⑤（次の
  呼び出しで自動でつなぎ直す。条件はDECISIONSの⑤のA〜G）、⑧（clientが判断したpairingの期限切れは`pair_expired`と同じ意味。
  serverのerrorの形は作らない。どちらが判断したかが分かる）
- 値と設定の仕方（timeoutの長さ、backoffの値）は言語ごと。fixtureで値を決めない

## PRを2つに分ける

1. **今のopsで表せるもの（先に）**：C#が最初の縦sliceで使うので、先にmergeする
   - 互換判定の後のclose：成功形のhelloの応答をclientが互換でないと判定し、次のrequestを送らずに閉じ、applicationへ失敗を
     返す。今のF1-HE-04、05のexpectedへ足すか、新しいcaseにするかは、toolingが選び、理由を返す
   - ②の残り：JSONは閉じているがLFの無い末尾のままEOFになり、応答にしない（F1-FR-05とF1-CL-03を合わせた形）。socketの
     errorと、自分で閉じたときの、応答待ちの回収。今のopsで表せないものがあれば、2へ回す
2. **新しいopsが要るもの**：`F1_E2_PROPOSALS_ja.md`の「追加案の返却」の表を形にする
   - applicationの呼び出しと、その結果（request idを持たない呼び出しの「未送信」を含む）の表し方
   - clientのtimeoutの設定に結びつく仮想の時計（期限の直前と到達を、値を決めずに表す）
   - 「送らないこと」を確かめる区間（④、⑤の旧requestの自動の再送）
   - notification（FASTの`world.setBlock`）と、接続ごとの観測（どの接続の互換判定か、どの接続の設置まで`connection.flush`が
     保証するか）
   - clientが判断して終わるpairing（⑧）。F1-AU-02は、serverが期限切れを返す経路として今のまま残す
   - caseは、③の期限と途中の受信、④、⑤の`build`の復元、つなぎ直せなかった呼び出し、旧FASTとflush、つなぎ直した
     helloでの非互換、⑧。⑤のA〜Gの残り（handleとcursorの失効、eventを失った知らせ、`auth_required`で止まる、一回の
     つなぎ直しへまとめる、backoffのばらつき、生存確認）は、表せるものを足し、表せないものは理由を返す
   - schemaの版を上げるか（`client-bootstrap-v1.schema.json`を広げるか、v2にするか）は、toolingが選び、理由を返す。
     今のconsumerが読めなくなるなら、そう書く

## 進め方

- 既定のbranchへのPRにして、CIが通ったら、担当がmergeしてよい。tag、Release、公開のworkflowの実行はしない
- 今の48 caseは変えない。直したいところが見つかったら、変えずに返す（1で、F1-HE-04、05を直すと選んだときは除く）
- 決まっていないことは、fixtureで決めない。決める必要が出たら、決めずに返す
- 足したcaseのfileの`knowledge_contract.commit`は、この依頼が入ったknowledgeのcommitにする

## 返却

PRごとに：

- 実際に読んだknowledge commit、PRの番号、merge commit、CIのrun ID
- 変えたfileの一覧（bytes、SHA-256）、足したcaseのIDとcaseの数
- 足したopsと`expected`の欄（2）と、そう決めた理由。schemaの版の扱い
- 表せずに残したことと、その理由

## coordinatorがすること

- 返却をGitHubのAPI（PR、merge commit、CI、fileのbytes）で照合し、Protocol Inventoryの共有fixtureの行を直す
- 1のmerge commitをC#へ、2のmerge commitをTypeScriptへ伝える。ほかのclientへは、固定し直しの票を作る

## 返却と照合（2026-11-12）

tooling担当はknowledge `076a127a22eaf0188c1d13822bfd55bfeee9ec38`を読んだ（この票の本文は今と同じ）。2つのPRを、担当が2026-11-12に
mergeした。coordinatorはGitHubのAPIで、PR、merge commit、CI、変わったfileのbytesとSHA-256を確かめた。

### 1（今のopsで表せるもの）

minecraft-remote-tooling PR #8（head `b4788af1045a409307c3216586137bfaf789b509`、base `36ebe9e63e4f0afcf949eae998832f68209b8119`）を
merge commit `d2691cdafb3b7548a4c26960184266c44bfcbd93`でmergeした。CIはPRのrun `43067599680`、merge後のrun `43067993877`とも成功。

| file（`packages/protocol/`の下） | bytes | SHA-256 |
| --- | ---: | --- |
| `F1_E2_PROPOSALS_ja.md` | 10,006 | `5a8c5fffb3c75b0a9f6ffec02b2d5212b854056cf8cb00ce0939c5588589b58b` |
| `README.md` | 13,072 | `99a2db475b54520c1010e5796d1c5499251ea031849eb65c76ea88888e4ab149` |
| `test/client-bootstrap-owner-fixture.test.ts` | 9,804 | `b40da20dee3c9e45edf51fab98023e2fb4be7d51cdfa1f3652481942a8436ed5` |
| `test/fixtures/client-bootstrap-close-v23.2.1.json` | 20,879 | `2abb6f48942e1dc7bc42014ba016c3d08a6632c59445c048b008a4c411ea1e30` |
| `test/fixtures/client-bootstrap-hello-v23.2.1.json` | 26,046 | `caf24ad5382e411ba54172b05d6020fc59fc429dc0251ff28db3908b4189784e` |
| `test/fixtures/client-bootstrap-v1.schema.json` | 11,465 | `4dcce4bc0a63c5e2536411e5276a85ceb8fa20bf5fef64ce2f7a2b8deb069774` |

- 足したcase：F1-HE-11、12（成功形のhelloの応答を、clientが互換でないと判定して閉じる。majorが違う、serverのminorが小さい）、
  F1-CL-07（JSONは閉じているがLFの無い末尾のままEOFになり、応答にしない）、F1-CL-08（自分で閉じた時に、応答待ちをすべて完了
  不明にする）。v1は52 case（helloが12、closeが8）。前の48 caseは変わっていない
- HE-04、05を直さずに新しいcaseへ分けた理由：今のconsumerの互換判定だけの期待値を変えずに、自分で閉じることとapplicationへの
  失敗までを別に確かめるため。HE-11、12は`application_failure: { source: "client", kind: "incompatible_protocol" }`を期待する
- socketのerrorはv1にopが無いので、2へ回した。ほかに、1で表せずに残したものは無い

### 2（新しいopsが要るもの）

minecraft-remote-tooling PR #9（head `ee61d3ee87dbb928c4307efb5e201259c2b8bd02`、base `d2691cd`）をmerge commit
`0d120e5ea1942178983fd0496827df7e7976f4e8`でmergeした（`main`の先頭）。CIはPRのrun `43070183866`、merge後のrun `43070626103`とも成功。

| file（`packages/protocol/`の下） | bytes | SHA-256 |
| --- | ---: | --- |
| `CLIENT_BOOTSTRAP_V2_ja.md` | 13,889 | `777911c1a356189b486a3367f330555511c0ef5422d91767f4939c62badbbf51` |
| `F1_E2_PROPOSALS_ja.md` | 10,159 | `48da4a92369b6fc12268cebd6e7feb7ae1b5cad7db6794ee932c7c797321d287` |
| `README.md` | 13,732 | `ac80f2d2bb16158ab139b2e5e3755b3665e59dee382caf3ceb51dbb5a2fa1e60` |
| `test/client-bootstrap-operations-fixture.test.ts` | 5,777 | `88f3d5d49a6c12c6c34e5d9ccd1df319f4dc7778619c125ad8b9d32c7b2ee71e` |
| `test/fixtures/client-bootstrap-operations-v23.2.1.json` | 66,029 | `3ccc97e4c80dbf51a0de9c27ef4e974fffa1ee7ec1708aeb7a49ffe14b8366a4` |
| `test/fixtures/client-bootstrap-v2.schema.json` | 19,423 | `f533de2755974147dd3d7c8f61fa3b190fc5031188a67d648b876ee33f979a77` |

- 足したcase：v2の`client-bootstrap-operations-v23.2.1.json`に、F1-OP-01〜12（socketのerror、③の期限と途中の受信、④、⑤の
  `build`の復元とつなぎ直せなかった呼び出し、旧FASTとflush、つなぎ直したhelloでの非互換、⑧、handleとcursorの失効、
  `auth_required`で止まる、一回のつなぎ直しへまとめる、生存確認で切れたと分かった後）。v1の6 fileと52 caseは変わっていない
- 足したops：applicationの入力（`app_connect`、`app_call`）と、その結果の観測（`expect_connect`、`expect_send`）。`socket_error`、
  `liveness_lost`、`advance_clock`（clientの`receive_idle`のtimeoutか、pairingの`expires_in`に対する分数で進め、秒数を決めない）、
  `observe`（途中の期待値）、`seed_epoch_state`（test adapterが取得済みのhandle、cursor、catalogのcacheを用意する。wireではない）。
  `expected.calls`は呼び出しごとの結果（未送信、完了不明、serverのerror、clientが判断したpairingの期限切れなど）と判断元を持ち、
  localな失敗にcodeとreasonを付けられないことをschemaと負例で確かめる
- schemaの版：今の対話と同じ方法では読めないので、`mcremote.client-bootstrap.v2`と`client-bootstrap-v2.schema.json`を別に足した。
  fileを名前で読むconsumerは続けて使える。`client-bootstrap-*-v23.2.1.json`をglobしてすべてv1として読むconsumerは、新しいfileを
  読めない（schemaで分けるか、v1の一覧を固定する）
- 表せずに残したもの：⑤Eの実際のthreadの競合（OP-10は重なりだけを表す）、⑤Fのbackoffのばらつきと延長（値も式も言語ごと）、
  ⑤Gで何を使ってどれだけ待って生存を確かめるか（OP-12は、切れたと判断した後だけ）
- 伝えたもの：1のmerge commitをC#へ、2のmerge commitをTypeScriptへ伝えた。C#は`d2691cd`で、TypeScriptは`0d120e5`で
  52 caseを通した（`00-hub/polyglot-csharp-start-instructions_ja.md`と`00-hub/polyglot-f1-e2-repin-instructions_ja.md`の
  「返却と照合（2026-11-12）」）

### 返却の後に、clientから届いたcaseへの指摘

- F1-AU-07：caseは最初の接続のEOFで終わるが、⑦のclientはその後、tokenなしのhelloを送る。どこで観測を終えるかを書いてほしい
  （Java、TypeScript）
- F1-OP-08：pairingを、helloと同じ接続で始める形になっている。AU-01、02は別の接続で、wire「6.5」はどちらでもよい。TypeScriptは
  いつも別の接続でpairingするので、OP-08をtodoにした
- v2の`expected`の「書いた行だけを比べる」の読み方を、説明に書いてほしい（TypeScript。OP-04、06でsessionが変わるのに
  `session_changed`を書いていないことから、そう読んだ）
- 承認を待つ間に、McRemoteが認証前のTCPを閉じ、clientが同じ`pairing_id`のpollを新しいTCPで続ける流れのcaseが無い（C#が実機で
  見た）
- toolingへ頼むかは、human ownerが決める（hub NOTES 2026-11-12の「多言語Client LibraryのE2を各clientへ入れる」の行）
